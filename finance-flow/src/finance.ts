import type { FinanceState, Transaction } from "./domain";

export const formatMoney = (cents: number): string =>
  new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD",
    maximumFractionDigits: 0,
  }).format(cents / 100);

export const parseMoney = (value: string): number => {
  if (!/^\d+(\.\d{1,2})?$/.test(value.trim()))
    throw new Error("Enter a valid amount with up to two decimal places.");
  const amount = Number(value);
  if (!Number.isFinite(amount) || amount <= 0)
    throw new Error("Enter an amount greater than zero.");
  return Math.round(amount * 100);
};

export const isValidDate = (value: string): boolean => {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
};

export const monthKey = (date: Date = new Date()): string =>
  `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;

export const transactionsForMonth = (
  transactions: Transaction[],
  month: string,
): Transaction[] =>
  transactions.flatMap((transaction) => {
    const sourceMonth = transaction.date.slice(0, 7);
    if (sourceMonth === month) return [transaction];
    if (!transaction.recurring || sourceMonth > month) return [];
    const lastDay = new Date(
      Number(month.slice(0, 4)),
      Number(month.slice(5, 7)),
      0,
    ).getDate();
    const day = Math.min(Number(transaction.date.slice(8, 10)), lastDay);
    return [
      {
        ...transaction,
        date: `${month}-${String(day).padStart(2, "0")}`,
      },
    ];
  });

export const summarise = (state: FinanceState, month: string) => {
  const transactions = transactionsForMonth(state.transactions, month);
  const incomeCents = transactions
    .filter(({ kind }) => kind === "income")
    .reduce((sum, { amountCents }) => sum + amountCents, 0);
  const expenseCents = transactions
    .filter(({ kind }) => kind === "expense")
    .reduce((sum, { amountCents }) => sum + amountCents, 0);
  const balanceCents = incomeCents - expenseCents;
  const savingsRate =
    incomeCents > 0
      ? Math.max(0, calculateGoalContribution(state) / incomeCents)
      : 0;
  const goalContributionCents = calculateGoalContribution(state);
  const safeToSpendCents = Math.max(
    0,
    balanceCents - goalContributionCents - state.settings.bufferCents,
  );
  const weeklyCents = Math.floor(safeToSpendCents / 4.345);
  const categoryTotals = transactions
    .filter(({ kind }) => kind === "expense")
    .reduce<Record<string, number>>((totals, transaction) => {
      totals[transaction.category] =
        (totals[transaction.category] ?? 0) + transaction.amountCents;
      return totals;
    }, {});
  return {
    transactions,
    incomeCents,
    expenseCents,
    balanceCents,
    goalContributionCents,
    savingsRate,
    safeToSpendCents,
    weeklyCents,
    categoryTotals,
  };
};

function calculateGoalContribution(state: FinanceState): number {
  return state.goals.reduce(
    (sum, goal) =>
      sum +
      Math.max(
        0,
        Math.min(
          goal.targetCents - goal.savedCents,
          Math.round(goal.targetCents / 12),
        ),
      ),
    0,
  );
}

export const validateTransaction = (
  candidate: Omit<Transaction, "id" | "amountCents"> & { amount: string },
): string[] => {
  const errors: string[] = [];
  if (!candidate.description.trim()) errors.push("Description is required.");
  try {
    parseMoney(candidate.amount);
  } catch (error) {
    errors.push((error as Error).message);
  }
  if (!isValidDate(candidate.date)) errors.push("Choose a valid date.");
  if (!candidate.category) errors.push("Choose a category.");
  if (!["income", "expense"].includes(candidate.kind))
    errors.push("Choose a valid transaction type.");
  return errors;
};
