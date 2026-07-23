import { emptyState, type FinanceState } from "./domain";

const STORAGE_KEY = "finance-flow:v1";

export const isFinanceState = (value: unknown): value is FinanceState => {
  if (!value || typeof value !== "object") return false;
  const state = value as Partial<FinanceState>;
  return (
    state.version === 1 &&
    Array.isArray(state.transactions) &&
    state.transactions.every(
      (transaction) =>
        transaction &&
        typeof transaction.id === "string" &&
        typeof transaction.description === "string" &&
        Number.isSafeInteger(transaction.amountCents) &&
        transaction.amountCents > 0 &&
        ["income", "expense"].includes(transaction.kind) &&
        typeof transaction.category === "string" &&
        typeof transaction.date === "string" &&
        typeof transaction.recurring === "boolean",
    ) &&
    Array.isArray(state.goals) &&
    state.goals.every(
      (goal) =>
        goal &&
        typeof goal.id === "string" &&
        typeof goal.name === "string" &&
        Number.isSafeInteger(goal.targetCents) &&
        goal.targetCents > 0 &&
        Number.isSafeInteger(goal.savedCents) &&
        goal.savedCents >= 0 &&
        typeof goal.targetDate === "string",
    ) &&
    !!state.settings &&
    state.settings.currency === "AUD" &&
    Number.isSafeInteger(state.settings.bufferCents) &&
    state.settings.bufferCents >= 0
  );
};

export const migrateState = (value: unknown): FinanceState | null => {
  if (isFinanceState(value)) return value;
  if (!value || typeof value !== "object") return null;
  const legacy = value as Record<string, unknown>;
  if (
    legacy.version === undefined &&
    Array.isArray(legacy.transactions) &&
    Array.isArray(legacy.goals)
  ) {
    const migrated = {
      version: 1,
      transactions: legacy.transactions,
      goals: legacy.goals,
      settings: legacy.settings ?? emptyState().settings,
    };
    return isFinanceState(migrated) ? migrated : null;
  }
  return null;
};

export const loadState = (): FinanceState => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return emptyState();
    const parsed: unknown = JSON.parse(stored);
    return migrateState(parsed) ?? emptyState();
  } catch {
    return emptyState();
  }
};

export const saveState = (state: FinanceState): void =>
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));

export const exportState = (state: FinanceState): void => {
  const blob = new Blob([JSON.stringify(state, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `finance-flow-${new Date().toISOString().slice(0, 10)}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
};

export const parseImport = (content: string): FinanceState => {
  const parsed: unknown = JSON.parse(content);
  const migrated = migrateState(parsed);
  if (!migrated)
    throw new Error("That file is not a valid Finance Flow v1 backup.");
  return migrated;
};
