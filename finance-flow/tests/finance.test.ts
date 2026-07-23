import { describe, expect, it } from "vitest";
import { emptyState, type FinanceState } from "../src/domain";
import {
  isValidDate,
  monthKey,
  parseMoney,
  summarise,
  transactionsForMonth,
  validateTransaction,
} from "../src/finance";
import {
  isFinanceState,
  loadState,
  migrateState,
  parseImport,
  saveState,
} from "../src/storage";

describe("money", () => {
  it("converts decimal input to integer cents", () =>
    expect(parseMoney("12.34")).toBe(1234));
  it("rejects zero and invalid amounts", () => {
    expect(() => parseMoney("0")).toThrow();
    expect(() => parseMoney("nope")).toThrow();
    expect(() => parseMoney("1.999")).toThrow();
  });
});

describe("dates and recurrence", () => {
  it("uses a deterministic local month key", () =>
    expect(monthKey(new Date(2026, 6, 23))).toBe("2026-07"));
  it("rejects impossible calendar dates", () => {
    expect(isValidDate("2026-02-28")).toBe(true);
    expect(isValidDate("2026-02-30")).toBe(false);
  });
  it("projects recurring transactions into later months and clamps the day", () => {
    const transaction = {
      id: "rent",
      description: "Rent",
      amountCents: 100,
      kind: "expense" as const,
      category: "Housing",
      date: "2026-01-31",
      recurring: true,
    };
    expect(transactionsForMonth([transaction], "2026-02")[0].date).toBe(
      "2026-02-28",
    );
    expect(transactionsForMonth([transaction], "2025-12")).toEqual([]);
  });
});

describe("cash-flow summary", () => {
  const state: FinanceState = {
    ...emptyState(),
    settings: { currency: "AUD", bufferCents: 10_000 },
    transactions: [
      {
        id: "1",
        description: "Pay",
        amountCents: 300_000,
        kind: "income",
        category: "Other",
        date: "2026-07-01",
        recurring: true,
      },
      {
        id: "2",
        description: "Rent",
        amountCents: 120_000,
        kind: "expense",
        category: "Housing",
        date: "2026-07-02",
        recurring: true,
      },
      {
        id: "3",
        description: "Old bill",
        amountCents: 99_000,
        kind: "expense",
        category: "Other",
        date: "2026-06-02",
        recurring: false,
      },
    ],
  };

  it("limits calculations to the selected month", () => {
    const result = summarise(state, "2026-07");
    expect(result.incomeCents).toBe(300_000);
    expect(result.expenseCents).toBe(120_000);
    expect(result.balanceCents).toBe(180_000);
    expect(result.safeToSpendCents).toBe(170_000);
    expect(result.weeklyCents).toBe(39_125);
    expect(result.savingsRate).toBe(0);
    expect(result.categoryTotals).toEqual({ Housing: 120_000 });
  });

  it("never produces a negative safe-to-spend value", () => {
    expect(
      summarise(
        { ...state, settings: { currency: "AUD", bufferCents: 500_000 } },
        "2026-07",
      ).safeToSpendCents,
    ).toBe(0);
  });
});

describe("validation and backups", () => {
  it("returns useful transaction errors", () => {
    expect(
      validateTransaction({
        description: "",
        amount: "-1",
        kind: "expense",
        category: "",
        date: "bad",
        recurring: false,
      }),
    ).toHaveLength(4);
  });
  it("accepts the current persisted schema", () => {
    expect(isFinanceState(emptyState())).toBe(true);
    expect(parseImport(JSON.stringify(emptyState()))).toEqual(emptyState());
  });
  it("rejects unknown backup schemas", () =>
    expect(() => parseImport('{"version":2}')).toThrow());
  it("rejects malformed nested records", () => {
    expect(
      isFinanceState({
        ...emptyState(),
        transactions: [{ id: "broken", amountCents: "100" }],
      }),
    ).toBe(false);
  });
  it("migrates valid unversioned backups", () => {
    const { version: _version, ...legacy } = emptyState();
    expect(migrateState(legacy)).toEqual(emptyState());
  });
  it("round-trips state through browser storage", () => {
    const values = new Map<string, string>();
    Object.defineProperty(globalThis, "localStorage", {
      configurable: true,
      value: {
        getItem: (key: string) => values.get(key) ?? null,
        setItem: (key: string, value: string) => values.set(key, value),
      },
    });
    const state = {
      ...emptyState(),
      settings: { currency: "AUD" as const, bufferCents: 25_000 },
    };
    saveState(state);
    expect(loadState()).toEqual(state);
  });
});
