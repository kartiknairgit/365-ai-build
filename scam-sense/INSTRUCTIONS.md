# ScamSense Internal Instructions

This document is the living build log and internal planning record for the ScamSense subproject.

## Current Status

The v0.1 deterministic rule engine, Streamlit experience, tests, deployment configuration and release documentation are implemented. ScamSense remains a lightweight educational prototype with no external analysis API, authentication, database or message history.

## Vision

ScamSense is an explainable scam-risk assistant. Users paste a suspicious SMS, email, marketplace message, job offer, crypto DM, rental message, or urgent family text. ScamSense identifies scam risk signals, explains why they matter, and suggests the safest next step.

## Target Users

- Everyday users who receive suspicious messages and want plain-language guidance
- Families helping older relatives or less technical users evaluate messages
- Marketplace buyers and sellers checking unusual payment or shipping requests
- Job seekers evaluating suspicious recruiter messages or offers
- People who want a second opinion before clicking links, sending money, or sharing personal information

## Differentiator

ScamSense is not positioned as the first scam detector. Existing tools already scan messages and links.

The differentiator is transparent reasoning, family-friendly explanations, and safety-first next steps. ScamSense should help users understand why a message is risky rather than only returning a verdict.

## MVP Scope

The v0.1 MVP should focus on a rule-based message analysis flow:

- Accept pasted suspicious-message text
- Detect common scam-risk signals
- Assign a low, medium, or high risk level
- Explain triggered signals in plain language
- Recommend safe next steps
- Avoid definitive claims
- Include an appropriate disclaimer
- Include focused tests for scoring and explanation behavior

## Non-Goals for v0.1

- No external API calls
- No AI-generated analysis
- No link fetching or URL reputation lookup
- No user accounts
- No message storage
- No browser extension
- No live public deployment is created by the repository alone
- No claim that ScamSense can prove whether a message is fraudulent

## Standard GitHub Workflow

Every meaningful ScamSense task should follow this workflow:

1. Sync `main`.
2. Confirm or create a GitHub issue before starting work.
3. Create a focused branch from `main`.
4. Make a small, meaningful change.
5. Update progress documentation, especially the `INSTRUCTIONS.md` build log.
6. If new scope is discovered, create a new GitHub issue instead of silently expanding the current task.
7. Keep GitHub milestones accurate.
8. Push the branch.
9. Open a PR linked to the issue using `Closes #issue-number`.
10. Review the diff.
11. Merge the PR.
12. Delete the branch.
13. Pull `main` again before starting the next task.

## Codex Operating Rules

- Codex must keep work inside `scam-sense/` unless explicitly instructed otherwise.
- Codex must not commit unless explicitly asked.
- Codex must show changed files and a summary after each task.
- Codex must not implement beyond the active issue scope.
- Codex must update the build log when meaningful progress is made.
- Codex must suggest a new issue when it finds new scope.
- Codex must avoid fake or busywork commits.
- Commits should be meaningful and tied to real progress.
- Daily goal is at least 10 meaningful commits, not spam commits.

## Build Log

### 2026-07-23

- Implemented the typed, deterministic signal detector, category classifier, and documented 0–100 risk scoring model.
- Expanded the fictional fixture library with rental, tax/government, lower-risk, and ambiguous examples.
- Added threshold, detector, category, regression, and safety-language tests plus isolated ScamSense CI.
- Added the Streamlit input and result experience with fictional examples, clear/reset controls, accessible text-labelled risk presentation, parent-friendly explanations, and empty/lower-risk/high-risk states.
- Added cautious Australian guidance using verified Scamwatch and cyber.gov.au reporting and recovery sources.
- Added pinned Streamlit deployment dependencies, a clean-environment startup check, deployment documentation, and a portfolio-ready README with an illustrative generated preview.

### 2026-07-09

- Created the initial `scam-sense/` subproject structure.
- Added public-facing project overview, internal instructions, research notes, product plan, and safe fictional sample messages.
- Kept the setup limited to planning and documentation with no application code.
- Added GitHub project planning doc.
- Defined milestones, labels, Kanban columns, and initial issue backlog.
- Added safety policy.
- Defined language constraints, privacy expectations, and user-protection rules.
- Added v0.1 architecture notes.
- Defined planned modules, data flow, output schema, and testing strategy.
- Added GitHub issue templates for feature, bug, and research tasks.
- Prepared repository for structured Kanban workflow.
- Started Issue #1: Define scam signal taxonomy.
- Added initial signal taxonomy documentation.
- Merged the first issue-driven PR for the signal taxonomy.
- Added standard GitHub workflow instructions for future ScamSense work.
- Started Issue #2: Design risk scoring model.
- Added initial risk scoring model documentation.
