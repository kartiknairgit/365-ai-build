# Product Plan

## v0.1 Rule-Based MVP

Goal: Build a minimal, testable scam-risk analyzer without external services.

Planned capabilities:

- Accept a plain-text message as input
- Detect common scam-risk signals with transparent rules
- Score the message as low, medium, or high risk
- Return concise explanations for each triggered signal
- Recommend safe next steps based on risk level
- Use cautious language and avoid definitive fraud claims
- Include tests for representative message categories

## v0.2 Streamlit Demo Polish

Goal: Add a simple local demo interface after the core logic is stable.

Planned capabilities:

- Text area for pasted messages
- Clear risk result display
- Signal-by-signal explanation panel
- Safety next-step section
- Friendly disclaimer
- Basic sample-message selector for demos
- Lightweight visual polish without changing the core analysis contract

## v0.3 AI Explanation Layer

Goal: Explore AI-assisted explanations while preserving safety and transparency.

Planned capabilities:

- Use the rule-based analyzer as the source of truth
- Generate friendlier summaries from triggered signals
- Keep risk scoring deterministic
- Add prompt and response tests for safety language
- Avoid unsupported claims or definitive scam labels
- Clearly separate deterministic detection from generated explanation

## v1.0 Public Demo

Goal: Make ScamSense usable as a public-facing demo with clear boundaries.

Planned capabilities:

- Public demo deployment
- Strong disclaimer and privacy notice
- No unnecessary message retention
- Abuse-resistant input handling
- Polished example library
- Documentation for limitations and appropriate use
- Clear routing to official reporting and verification resources

## Rough GitHub Kanban Issue List

### Backlog

- Define initial scam-risk signal taxonomy
- Draft scoring rubric for low, medium, and high risk
- Create expected output schema for analysis results
- Write fictional sample-message fixtures
- Research safe wording for disclaimers and next steps
- Identify official verification and reporting resources for documentation

### Ready

- Implement rule definitions for urgency, impersonation, payment pressure, suspicious links, and sensitive-info requests
- Add unit tests for each rule category
- Add tests for risk-level thresholds
- Add tests to ensure output avoids definitive scam claims
- Create CLI or function-level analysis entry point

### In Progress

- None yet

### Review

- None yet

### Done

- Create initial project structure
- Add README
- Add internal instructions
- Add research notes
- Add product plan
- Add fictional sample messages
