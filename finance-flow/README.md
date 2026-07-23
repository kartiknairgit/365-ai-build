# Finance Flow

Finance Flow is a privacy-first personal cash-flow planner. It helps people turn recurring income, bills, everyday spending, and savings goals into a clear monthly picture and a practical weekly spending guide.

## v1.0 goals

- Capture income, expenses, and savings goals
- Categorise and filter transactions
- Show monthly cash flow, category totals, and savings progress
- Calculate a safe-to-spend weekly amount
- Persist data locally and support JSON import/export
- Provide responsive, accessible, keyboard-friendly interactions
- Work without accounts, analytics, external APIs, or financial-data connections

Finance Flow is an educational planning tool, not financial advice. Users remain responsible for verifying their figures and making financial decisions.

## Run locally

Requires Node.js 20 or newer.

```bash
cd finance-flow
npm install
npm run dev
```

Available quality commands:

```bash
npm run format
npm run lint
npm test
npm run build
npm run check
```

All application data is stored in the current browser's local storage. Export a JSON backup before clearing browser data.

## Calculation model

The selected month's remaining cash is income minus expenses. Finance Flow then reserves a configurable buffer and an estimated monthly contribution for each savings goal. The amount left is divided by 4.345 to create the weekly guide. The guide never falls below zero and is intended as a planning aid, not a recommendation.

Recurring transactions are projected from their first date into later selected months. Dates at the end of a long month are clamped to the final day of shorter months.

## Privacy and data safety

Finance Flow has no account, analytics, bank feed, server storage, or external financial API. Data is saved only in browser local storage. JSON imports replace the current plan, so export a backup first if the existing data matters. Reset permanently removes the plan from that browser after confirmation.

## Deployment

`npm run build` writes a static site to `finance-flow/dist/`. The relative asset base supports hosting from a subdirectory:

- GitHub Pages: upload the `dist` build artifact from the Finance Flow Actions workflow to a Pages deployment workflow or deploy it with your preferred Pages action.
- Netlify or Cloudflare Pages: set the base directory to `finance-flow`, build command to `npm run build`, and publish directory to `dist`.
- Any static host: serve the contents of `dist` over HTTPS.

The repository workflow runs formatting, type checks, tests, and a production build for Finance Flow pull requests and uploads `dist` as an artifact.

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for product boundaries, architecture, workflow, and the v1.0 backlog.
