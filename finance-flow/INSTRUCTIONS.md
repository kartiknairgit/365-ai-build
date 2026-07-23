# Finance Flow Internal Instructions

## Mission

Build a calm, privacy-first personal cash-flow planner that makes the question “what can I safely spend?” easier to answer. Finance Flow converts income, recurring bills, flexible expenses, and savings goals into transparent monthly summaries and a practical weekly allowance.

## Product principles

- Local-first: no account, bank connection, analytics, or server-side storage in v1.0.
- Explainable: calculations must be deterministic, visible, and tested.
- Supportive: use neutral language and avoid shame, pressure, or claims of financial advice.
- Accessible: core workflows must work with keyboard navigation, clear labels, and responsive layouts.
- Portable: users must be able to export and restore their own data.

## v1.0 scope

Finance Flow v1.0 includes a responsive single-page application, local persistence, transaction management, categories, dashboard summaries, savings goals, safe-to-spend calculations, JSON import/export, validation, empty states, accessibility checks, tests, and deployment documentation.

It excludes authentication, cloud sync, bank feeds, investment or tax advice, multi-currency conversion, AI recommendations, and external APIs.

## Architecture

- TypeScript application under `finance-flow/`
- Pure domain functions for money, dates, summaries, and safe-to-spend calculations
- Browser storage behind a small repository interface
- Components consume typed selectors rather than duplicating finance logic
- Unit and integration tests cover calculations and critical workflows

## Required GitHub workflow

Every issue follows: sync `main` → create a focused branch → implement only the issue scope → test → update this build log when meaningful → commit → push → open a PR with `Closes #…` → review checks and diff → merge → delete the branch → pull `main`.

All Finance Flow issue titles start with `[Finance Flow]`, use the `project:finance-flow` label, and belong to the `Finance Flow v1.0` milestone.

## v1.0 issue plan

1. Establish project foundation and documentation.
2. Scaffold the TypeScript web application and quality scripts.
3. Define typed finance domain models and seed data.
4. Add precise money and date utilities.
5. Implement transaction validation.
6. Implement cash-flow summary calculations.
7. Implement safe-to-spend calculations.
8. Add local persistence with schema versioning.
9. Build the application shell and responsive navigation.
10. Build dashboard summary cards.
11. Build transaction list, filters, and search.
12. Build add/edit/delete transaction workflows.
13. Build category spending breakdown.
14. Build savings-goal tracking.
15. Build monthly budget and weekly allowance views.
16. Add JSON export, import, and reset controls.
17. Add onboarding, demo data, and empty states.
18. Complete accessibility and responsive UX pass.
19. Add comprehensive unit and integration tests.
20. Finish release documentation, CI, and deployment readiness.

## Build log

### 2026-07-23

- Inspected and synced the existing repository and confirmed Finance Flow has no prior tracked implementation.
- Defined the mission, v1.0 boundaries, architecture, and 20-issue delivery plan.
- Added the isolated project documentation and root repository index entry.
- Implemented the TypeScript web application, typed domain model, finance calculations, validation, versioned local persistence, and fictional demo state.
- Added responsive dashboard, transaction management, search and filters, category breakdowns, savings goals, weekly guidance, backup and reset controls, onboarding, and accessible interaction states.
- Added automated domain and persistence tests plus production build checks.
- Completed transaction editing, recurring-month projection, configurable planning buffers, goal remaining balances, and stricter import validation with legacy-state migration.
- Added formatting and type-check scripts, pull-request CI with a deployable static artifact, and release, privacy, and deployment guidance.
