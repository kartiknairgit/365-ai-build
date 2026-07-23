export type TransactionKind = "income" | "expense";

export interface Transaction {
  id: string;
  description: string;
  amountCents: number;
  kind: TransactionKind;
  category: string;
  date: string;
  recurring: boolean;
}

export interface SavingsGoal {
  id: string;
  name: string;
  targetCents: number;
  savedCents: number;
  targetDate: string;
}

export interface Settings {
  currency: "AUD";
  bufferCents: number;
}

export interface FinanceState {
  version: 1;
  transactions: Transaction[];
  goals: SavingsGoal[];
  settings: Settings;
}

export const categories = [
  "Housing",
  "Food",
  "Transport",
  "Utilities",
  "Health",
  "Lifestyle",
  "Savings",
  "Other",
] as const;

export const emptyState = (): FinanceState => ({
  version: 1,
  transactions: [],
  goals: [],
  settings: { currency: "AUD", bufferCents: 10_000 },
});

const month = new Date().toISOString().slice(0, 7);

export const demoState = (): FinanceState => ({
  version: 1,
  settings: { currency: "AUD", bufferCents: 15_000 },
  transactions: [
    {
      id: crypto.randomUUID(),
      description: "Salary",
      amountCents: 420_000,
      kind: "income",
      category: "Other",
      date: `${month}-01`,
      recurring: true,
    },
    {
      id: crypto.randomUUID(),
      description: "Rent",
      amountCents: 168_000,
      kind: "expense",
      category: "Housing",
      date: `${month}-02`,
      recurring: true,
    },
    {
      id: crypto.randomUUID(),
      description: "Groceries",
      amountCents: 38_500,
      kind: "expense",
      category: "Food",
      date: `${month}-06`,
      recurring: false,
    },
    {
      id: crypto.randomUUID(),
      description: "Energy bill",
      amountCents: 14_400,
      kind: "expense",
      category: "Utilities",
      date: `${month}-09`,
      recurring: true,
    },
    {
      id: crypto.randomUUID(),
      description: "Train pass",
      amountCents: 18_000,
      kind: "expense",
      category: "Transport",
      date: `${month}-11`,
      recurring: false,
    },
  ],
  goals: [
    {
      id: crypto.randomUUID(),
      name: "Emergency buffer",
      targetCents: 300_000,
      savedCents: 125_000,
      targetDate: `${Number(month.slice(0, 4)) + 1}-06-30`,
    },
  ],
});
