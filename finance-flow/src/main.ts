import "./styles.css";
import {
  categories,
  demoState,
  emptyState,
  type FinanceState,
  type Transaction,
} from "./domain";
import {
  formatMoney,
  monthKey,
  parseMoney,
  summarise,
  validateTransaction,
} from "./finance";
import { exportState, loadState, parseImport, saveState } from "./storage";

let state = loadState();
let selectedMonth = monthKey();
let query = "";
let category = "All";
let editingTransactionId: string | null = null;

const app = document.querySelector<HTMLDivElement>("#app")!;

const escapeHtml = (value: string): string =>
  value.replace(
    /[&<>"']/g,
    (character) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      })[character]!,
  );

const render = (): void => {
  const summary = summarise(state, selectedMonth);
  const visibleTransactions = summary.transactions.filter(
    (transaction) =>
      (category === "All" || transaction.category === category) &&
      transaction.description.toLowerCase().includes(query.toLowerCase()),
  );
  const maxCategory = Math.max(...Object.values(summary.categoryTotals), 1);
  const goals = state.goals
    .map((goal) => {
      const progress = Math.min(
        100,
        Math.round((goal.savedCents / goal.targetCents) * 100),
      );
      return `<article class="goal">
      <div><strong>${escapeHtml(goal.name)}</strong><span>${progress}% funded</span></div>
      <progress value="${goal.savedCents}" max="${goal.targetCents}" aria-label="${escapeHtml(goal.name)} progress"></progress>
      <small>${formatMoney(goal.savedCents)} of ${formatMoney(goal.targetCents)} · target ${goal.targetDate}</small>
      <small>${formatMoney(Math.max(0, goal.targetCents - goal.savedCents))} remaining</small>
    </article>`;
    })
    .join("");

  app.innerHTML = `
    <header class="site-header">
      <a class="brand" href="#" aria-label="Finance Flow home"><span>F</span> Finance Flow</a>
      <p><span class="privacy-dot"></span> Your data stays in this browser</p>
    </header>
    <main id="main">
      <section class="hero">
        <div><p class="eyebrow">Monthly money, made clearer</p><h1>Know where your money can flow.</h1>
        <p>Plan income, bills and goals in one private view—then see a practical weekly spending guide.</p></div>
        <label>Viewing month<input id="month" type="month" value="${selectedMonth}" /></label>
      </section>
      ${state.transactions.length === 0 ? `<section class="welcome"><div><p class="eyebrow">Start with a clear slate</p><h2>Build your first monthly plan</h2><p>Add a transaction yourself or explore with fictional demo data. Nothing leaves this device.</p></div><button id="demo" class="secondary">Load demo plan</button></section>` : ""}
      <section class="metrics" aria-label="Monthly summary">
        <article><span>Income</span><strong>${formatMoney(summary.incomeCents)}</strong><small>for ${selectedMonth}</small></article>
        <article><span>Committed spending</span><strong>${formatMoney(summary.expenseCents)}</strong><small>${summary.transactions.filter((t) => t.kind === "expense").length} expenses</small></article>
        <article class="${summary.balanceCents < 0 ? "warning" : ""}"><span>Remaining cash</span><strong>${formatMoney(summary.balanceCents)}</strong><small>income minus expenses</small></article>
        <article class="accent"><span>Weekly guide</span><strong>${formatMoney(summary.weeklyCents)}</strong><small>after goals + ${formatMoney(state.settings.bufferCents)} buffer</small></article>
      </section>
      <div class="layout">
        <section class="panel transactions">
          <div class="panel-heading"><div><p class="eyebrow">Money in and out</p><h2>Transactions</h2></div><button id="add">+ Add transaction</button></div>
          <div class="filters">
            <label class="search">Search<input id="search" type="search" placeholder="Groceries, rent…" value="${escapeHtml(query)}" /></label>
            <label>Category<select id="category"><option>All</option>${categories.map((item) => `<option ${item === category ? "selected" : ""}>${item}</option>`).join("")}</select></label>
          </div>
          <div class="transaction-list">
          ${
            visibleTransactions.length
              ? visibleTransactions
                  .sort((a, b) => b.date.localeCompare(a.date))
                  .map(
                    (transaction) => `
            <article class="transaction">
              <span class="category-icon">${escapeHtml(transaction.category.slice(0, 1))}</span>
              <div><strong>${escapeHtml(transaction.description)}</strong><small>${transaction.category} · ${transaction.date}${transaction.recurring ? " · recurring" : ""}</small></div>
              <b class="${transaction.kind}">${transaction.kind === "income" ? "+" : "−"}${formatMoney(transaction.amountCents)}</b>
              <div class="transaction-actions">
                <button class="icon-button edit" data-id="${transaction.id}" aria-label="Edit ${escapeHtml(transaction.description)}">Edit</button>
                <button class="icon-button delete" data-id="${transaction.id}" aria-label="Delete ${escapeHtml(transaction.description)}">×</button>
              </div>
            </article>`,
                  )
                  .join("")
              : `<div class="empty"><strong>No matching transactions</strong><p>Add one or adjust the month and filters.</p></div>`
          }
          </div>
        </section>
        <aside>
          <section class="panel">
            <div class="panel-heading"><div><p class="eyebrow">Where it goes</p><h2>Spending</h2></div></div>
            <div class="breakdown">${
              Object.entries(summary.categoryTotals)
                .sort((a, b) => b[1] - a[1])
                .map(
                  ([name, cents]) => `
              <div><span>${escapeHtml(name)} <b>${formatMoney(cents)}</b></span><div class="bar"><i style="width:${Math.round((cents / maxCategory) * 100)}%"></i></div></div>`,
                )
                .join("") ||
              `<p class="muted">Category totals will appear here.</p>`
            }</div>
          </section>
          <section class="panel">
            <div class="panel-heading"><div><p class="eyebrow">Future you</p><h2>Savings goals</h2></div><button id="add-goal" class="text-button">+ Add</button></div>
            ${goals || `<p class="muted">Add a goal to include a monthly contribution in your weekly guide.</p>`}
          </section>
          <section class="panel data-tools">
            <h2>Your data</h2><p class="muted">Make a portable backup or restore one. Imports replace the current plan.</p>
            <label class="buffer-setting">Planning buffer (AUD)<input id="buffer" type="number" min="0" step="0.01" value="${(state.settings.bufferCents / 100).toFixed(2)}" /><small>Held back before the weekly guide is calculated.</small></label>
            <div><button id="export" class="secondary">Export JSON</button><label class="file-button">Import JSON<input id="import" type="file" accept="application/json" /></label><button id="reset" class="danger">Reset</button></div>
          </section>
        </aside>
      </div>
      <p class="disclaimer">Finance Flow is an educational planning tool, not financial advice. Check your figures before making decisions.</p>
    </main>
    <dialog id="transaction-dialog">
      <form id="transaction-form">
        <div class="dialog-heading"><div><p class="eyebrow">Cash-flow item</p><h2 id="transaction-dialog-title">Add transaction</h2></div><button type="button" class="icon-button close" aria-label="Close">×</button></div>
        <div id="form-errors" class="form-errors" role="alert"></div>
        <label>Description<input name="description" autocomplete="off" required /></label>
        <div class="form-grid"><label>Amount (AUD)<input name="amount" type="number" min="0.01" step="0.01" required /></label>
        <label>Type<select name="kind"><option value="expense">Expense</option><option value="income">Income</option></select></label></div>
        <div class="form-grid"><label>Category<select name="category">${categories.map((item) => `<option>${item}</option>`).join("")}</select></label>
        <label>Date<input name="date" type="date" value="${new Date().toISOString().slice(0, 10)}" required /></label></div>
        <label class="check"><input name="recurring" type="checkbox" /> This repeats monthly</label>
        <button type="submit">Save transaction</button>
      </form>
    </dialog>
    <dialog id="goal-dialog">
      <form id="goal-form">
        <div class="dialog-heading"><div><p class="eyebrow">A little at a time</p><h2>Add savings goal</h2></div><button type="button" class="icon-button close" aria-label="Close">×</button></div>
        <label>Goal name<input name="name" required /></label>
        <div class="form-grid"><label>Target amount<input name="target" type="number" min="1" step="0.01" required /></label><label>Already saved<input name="saved" type="number" min="0" step="0.01" value="0" required /></label></div>
        <label>Target date<input name="targetDate" type="date" required /></label>
        <button type="submit">Save goal</button>
      </form>
    </dialog>`;
  bindEvents();
};

const persist = (): void => {
  saveState(state);
  render();
};

const openTransactionDialog = (transaction?: Transaction): void => {
  editingTransactionId = transaction?.id ?? null;
  const dialog = document.querySelector(
    "#transaction-dialog",
  ) as HTMLDialogElement;
  const form = dialog.querySelector("form") as HTMLFormElement;
  (
    dialog.querySelector("#transaction-dialog-title") as HTMLElement
  ).textContent = transaction ? "Edit transaction" : "Add transaction";
  if (transaction) {
    (form.elements.namedItem("description") as HTMLInputElement).value =
      transaction.description;
    (form.elements.namedItem("amount") as HTMLInputElement).value = (
      transaction.amountCents / 100
    ).toFixed(2);
    (form.elements.namedItem("kind") as HTMLSelectElement).value =
      transaction.kind;
    (form.elements.namedItem("category") as HTMLSelectElement).value =
      transaction.category;
    (form.elements.namedItem("date") as HTMLInputElement).value =
      transaction.date;
    (form.elements.namedItem("recurring") as HTMLInputElement).checked =
      transaction.recurring;
  } else {
    form.reset();
    (form.elements.namedItem("date") as HTMLInputElement).value =
      `${selectedMonth}-01`;
  }
  dialog.showModal();
};

const bindEvents = (): void => {
  document
    .querySelector<HTMLInputElement>("#month")
    ?.addEventListener("change", (event) => {
      selectedMonth = (event.target as HTMLInputElement).value;
      render();
    });
  document
    .querySelector<HTMLInputElement>("#search")
    ?.addEventListener("input", (event) => {
      query = (event.target as HTMLInputElement).value;
      render();
      document.querySelector<HTMLInputElement>("#search")?.focus();
    });
  document
    .querySelector<HTMLSelectElement>("#category")
    ?.addEventListener("change", (event) => {
      category = (event.target as HTMLSelectElement).value;
      render();
    });
  document.querySelector("#demo")?.addEventListener("click", () => {
    state = demoState();
    persist();
  });
  document
    .querySelector("#add")
    ?.addEventListener("click", () => openTransactionDialog());
  document
    .querySelector("#add-goal")
    ?.addEventListener("click", () =>
      (document.querySelector("#goal-dialog") as HTMLDialogElement).showModal(),
    );
  document
    .querySelectorAll<HTMLButtonElement>(".close")
    .forEach((button) =>
      button.addEventListener("click", () => button.closest("dialog")?.close()),
    );
  document.querySelectorAll<HTMLButtonElement>(".edit").forEach((button) =>
    button.addEventListener("click", () => {
      const transaction = state.transactions.find(
        ({ id }) => id === button.dataset.id,
      );
      if (transaction) openTransactionDialog(transaction);
    }),
  );
  document.querySelectorAll<HTMLButtonElement>(".delete").forEach((button) =>
    button.addEventListener("click", () => {
      const transaction = state.transactions.find(
        ({ id }) => id === button.dataset.id,
      );
      if (transaction && confirm(`Delete “${transaction.description}”?`)) {
        state.transactions = state.transactions.filter(
          ({ id }) => id !== button.dataset.id,
        );
        persist();
      }
    }),
  );
  document
    .querySelector("#transaction-form")
    ?.addEventListener("submit", (event) => {
      event.preventDefault();
      const form = event.currentTarget as HTMLFormElement;
      const data = new FormData(form);
      const candidate = {
        description: String(data.get("description")),
        amount: String(data.get("amount")),
        kind: String(data.get("kind")) as Transaction["kind"],
        category: String(data.get("category")),
        date: String(data.get("date")),
        recurring: data.get("recurring") === "on",
      };
      const errors = validateTransaction(candidate);
      if (errors.length) {
        document.querySelector("#form-errors")!.textContent = errors.join(" ");
        return;
      }
      const nextTransaction = {
        ...candidate,
        id: editingTransactionId ?? crypto.randomUUID(),
        amountCents: parseMoney(candidate.amount),
      };
      if (editingTransactionId) {
        state.transactions = state.transactions.map((transaction) =>
          transaction.id === editingTransactionId
            ? nextTransaction
            : transaction,
        );
      } else {
        state.transactions.push(nextTransaction);
      }
      editingTransactionId = null;
      selectedMonth = candidate.date.slice(0, 7);
      form.closest("dialog")?.close();
      persist();
    });
  document.querySelector("#goal-form")?.addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.currentTarget as HTMLFormElement;
    const data = new FormData(form);
    const name = String(data.get("name")).trim();
    const targetDate = String(data.get("targetDate"));
    const saved = Number(data.get("saved"));
    if (!name || !targetDate || !Number.isFinite(saved) || saved < 0) {
      alert("Complete the goal with valid amounts and a target date.");
      return;
    }
    const targetCents = parseMoney(String(data.get("target")));
    const savedCents = Math.round(saved * 100);
    if (savedCents > targetCents) {
      alert("The amount saved cannot be greater than the target.");
      return;
    }
    state.goals.push({
      id: crypto.randomUUID(),
      name,
      targetCents,
      savedCents,
      targetDate,
    });
    form.closest("dialog")?.close();
    persist();
  });
  document
    .querySelector<HTMLInputElement>("#buffer")
    ?.addEventListener("change", (event) => {
      const value = Number((event.target as HTMLInputElement).value);
      if (!Number.isFinite(value) || value < 0) {
        alert("Enter a buffer of zero or more.");
        render();
        return;
      }
      state.settings.bufferCents = Math.round(value * 100);
      persist();
    });
  document
    .querySelector("#export")
    ?.addEventListener("click", () => exportState(state));
  document
    .querySelector<HTMLInputElement>("#import")
    ?.addEventListener("change", async (event) => {
      const file = (event.target as HTMLInputElement).files?.[0];
      if (!file) return;
      try {
        state = parseImport(await file.text());
        persist();
      } catch (error) {
        alert((error as Error).message);
      }
    });
  document.querySelector("#reset")?.addEventListener("click", () => {
    if (confirm("Reset all Finance Flow data in this browser?")) {
      state = emptyState();
      persist();
    }
  });
};

render();
