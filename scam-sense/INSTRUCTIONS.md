# ScamSense Internal Instructions

This document is the living build log and internal planning record for the ScamSense subproject.

## Current Status

Project setup and planning only.

The repository currently contains documentation, planning notes, placeholder source and test directories, and fictional sample messages. There is no application implementation, Streamlit interface, model integration, or external API call in this stage.

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

- No Streamlit app yet
- No external API calls
- No AI-generated analysis
- No link fetching or URL reputation lookup
- No user accounts
- No message storage
- No browser extension
- No production deployment
- No claim that ScamSense can prove whether a message is fraudulent

## Build Log

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
