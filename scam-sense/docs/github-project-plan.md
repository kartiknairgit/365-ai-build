# GitHub Project Plan

This document prepares ScamSense for a future GitHub Project board. It is planning only: no GitHub milestones, labels, project columns, or issues have been created yet.

## Proposed Milestones

### v0.1 Rule-Based MVP

Build the deterministic core of ScamSense: scam-signal detection, risk scoring, category classification, safety language, sample data, and tests.

### v0.2 Streamlit Demo Polish

Add a simple local Streamlit demo after the v0.1 core logic is stable. Focus on pasted-message input, clear result cards, explanation display, and demo-ready polish.

### v0.3 AI Explanation Layer

Explore AI-assisted explanation text while keeping rule-based detection and scoring as the source of truth. Add safety checks to avoid unsupported or definitive claims.

### v1.0 Public Demo

Prepare a public-facing demo with deployment, documentation, privacy expectations, safety guidance, and polished screenshots.

## Proposed Labels

### Area Labels

- `area:docs`
- `area:engine`
- `area:ui`
- `area:tests`
- `area:safety`
- `area:deploy`

### Priority Labels

- `priority:p0`
- `priority:p1`
- `priority:p2`

## Kanban Board Setup

- Backlog: captured work that is not ready to start.
- Ready: scoped issues with clear acceptance criteria.
- In Progress: actively being worked.
- Review: implementation or documentation is ready for review.
- Done: accepted and complete.

## Execution Workflow

ScamSense work should move through an issue to branch to PR to merge workflow. Each meaningful task should start from a scoped GitHub issue, be completed on a focused branch, be reviewed through a PR linked with `Closes #issue-number`, and then be merged back to `main` before the next task begins.

## Initial Issue Backlog

### Define scam signal taxonomy

Purpose: Establish the initial set of observable scam-risk signals that ScamSense can explain clearly.

Acceptance criteria:

- Defines core signals such as urgency, impersonation, suspicious links, payment pressure, secrecy, sensitive-info requests, and unrealistic offers.
- Includes a plain-language explanation for each signal.
- Identifies which signals are high confidence versus contextual.
- Avoids claiming that any single signal proves a message is a scam.

Suggested labels: `area:engine`, `area:safety`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Design risk scoring model

Purpose: Create a transparent scoring approach that maps detected signals to low, medium, or high risk.

Acceptance criteria:

- Defines risk levels and thresholds.
- Documents signal weights or severity rules.
- Explains how multiple weak signals combine.
- Includes guidance for cautious wording at each risk level.

Suggested labels: `area:engine`, `area:safety`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Build rule-based signal detector

Purpose: Implement the deterministic detector that finds scam-risk signals in pasted messages.

Acceptance criteria:

- Detects the initial taxonomy of signals.
- Returns structured signal results suitable for scoring and explanation.
- Handles empty, short, and long messages gracefully.
- Does not call external APIs or store user messages.

Suggested labels: `area:engine`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Add scam category classifier

Purpose: Group messages into broad scam categories to make results easier to understand.

Acceptance criteria:

- Supports categories such as delivery, bank alert, marketplace, crypto, job offer, rental, and family emergency.
- Allows an unknown or general category when confidence is low.
- Uses category as context, not proof.
- Includes examples for each supported category.

Suggested labels: `area:engine`, `area:safety`, `priority:p1`

Milestone: v0.1 Rule-Based MVP

### Create Streamlit input UI

Purpose: Provide a simple demo interface for pasting suspicious message text.

Acceptance criteria:

- Provides a text input area for suspicious messages.
- Includes a clear analyze action.
- Handles empty input with a friendly validation state.
- Does not change the core analysis contract.

Suggested labels: `area:ui`, `priority:p1`

Milestone: v0.2 Streamlit Demo Polish

### Build result card UI

Purpose: Present the risk level, key signals, and next steps in a clear result layout.

Acceptance criteria:

- Displays low, medium, or high risk clearly.
- Shows triggered signals with concise explanations.
- Shows recommended next steps.
- Includes disclaimer language near the result.

Suggested labels: `area:ui`, `area:safety`, `priority:p1`

Milestone: v0.2 Streamlit Demo Polish

### Add parent-friendly explanation output

Purpose: Make ScamSense explanations easy to share with family members or less technical users.

Acceptance criteria:

- Adds a concise plain-language summary.
- Avoids jargon and fear-based language.
- Uses cautious phrasing such as "looks risky" rather than "is definitely a scam."
- Includes a safe verification recommendation.

Suggested labels: `area:safety`, `area:docs`, `priority:p1`

Milestone: v0.1 Rule-Based MVP

### Add Australian safety/reporting guidance

Purpose: Provide practical next-step guidance for Australian users.

Acceptance criteria:

- References relevant Australian reporting and consumer-safety channels in documentation or guidance copy.
- Encourages users to verify through official channels.
- Avoids legal, financial, or law-enforcement advice claims.
- Keeps guidance concise and non-alarmist.

Suggested labels: `area:safety`, `area:docs`, `priority:p1`

Milestone: v1.0 Public Demo

### Add fictional sample message library

Purpose: Maintain safe fictional examples for demos, tests, and documentation.

Acceptance criteria:

- Includes fictional samples for delivery, bank alert, marketplace, crypto, job offer, rental, and family emergency scenarios.
- Uses clearly fake links and organizations.
- Notes that examples are fictional.
- Keeps samples suitable for future tests without real personal data.

Suggested labels: `area:docs`, `area:tests`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Add unit tests for signal detection

Purpose: Verify that the rule-based detector consistently identifies expected signals.

Acceptance criteria:

- Covers each signal in the initial taxonomy.
- Includes negative tests for messages that should not trigger specific signals.
- Tests edge cases such as empty input and mixed signal messages.
- Keeps fixtures fictional and safe.

Suggested labels: `area:tests`, `area:engine`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Add unit tests for risk scoring

Purpose: Verify that detected signals map to expected risk levels.

Acceptance criteria:

- Covers low, medium, and high risk outcomes.
- Tests combinations of weak and strong signals.
- Confirms output uses non-definitive language.
- Documents expected scoring behavior through test names or fixtures.

Suggested labels: `area:tests`, `area:engine`, `area:safety`, `priority:p0`

Milestone: v0.1 Rule-Based MVP

### Prepare Streamlit deployment

Purpose: Prepare the demo for hosting after the local interface is stable.

Acceptance criteria:

- Documents deployment target and required configuration.
- Confirms no secrets are committed.
- Adds deployment instructions.
- Checks that the app runs from a clean environment.

Suggested labels: `area:deploy`, `area:docs`, `priority:p2`

Milestone: v1.0 Public Demo

### Polish README with screenshots

Purpose: Improve the public project page once the demo UI exists.

Acceptance criteria:

- Adds current screenshots or GIFs of the demo.
- Explains the project value clearly.
- Documents limitations and disclaimer.
- Keeps setup instructions accurate.

Suggested labels: `area:docs`, `area:ui`, `priority:p2`

Milestone: v1.0 Public Demo
