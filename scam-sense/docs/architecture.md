# Architecture

This document describes the v0.1 architecture implemented for ScamSense as a rule-based scam-risk checker.

## 1. System Overview

ScamSense v0.1 will analyze pasted message text locally using deterministic rules. The system will identify scam-risk signals, estimate a risk level, classify the likely scam category when possible, and produce plain-language safety guidance.

The v0.1 architecture should prioritize:

- Explainable decisions
- Testable behavior
- Deterministic scoring
- Safety-first user guidance
- No message storage
- No external API calls

## 2. Planned Module Structure

The source modules are organized around the analysis pipeline:

```text
src/scamsense/
  normalization.py
  signal_taxonomy.py
  signal_detector.py
  category_classifier.py
  risk_scorer.py
  guidance.py
  analysis.py
```

`app.py` consumes only the composed `analyse_message` contract; detection, classification, scoring and guidance remain independently testable.

## 3. Data Flow

Planned v0.1 flow:

1. User pastes message.
2. Text is normalized.
3. Signal detector extracts red flags.
4. Category classifier identifies likely scam type.
5. Risk scorer calculates risk level.
6. Guidance generator produces safe next steps.
7. UI renders result card.

Detailed flow:

- The user provides raw message text through a future UI or function entry point.
- Input normalization prepares the text for analysis while preserving the original meaning.
- The signal detector checks the normalized text against the scam signal taxonomy.
- The category classifier uses detected phrases and signals to estimate the most likely scam type.
- The risk scorer combines signal severity and signal count into a low, medium, high, or critical risk level.
- The safety guidance generator creates next-step guidance based on risk level, category, and unsafe actions.
- The result formatter returns a consistent result object for future UI rendering.

## 4. Planned Modules

### Input Normalization

Purpose: Prepare pasted text for consistent analysis.

Responsibilities:

- Trim unnecessary whitespace
- Normalize casing for matching
- Preserve the original message for display when needed
- Handle empty or very short input
- Avoid storing raw user messages

### Scam Signal Taxonomy

Purpose: Define the supported red-flag signals and their explanation text.

Responsibilities:

- Define signals such as urgency, impersonation, suspicious links, payment pressure, secrecy, sensitive-information requests, unrealistic offers, and unusual payment methods
- Assign severity metadata to each signal
- Provide plain-language explanations
- Keep signal definitions auditable and easy to test

### Signal Detector

Purpose: Extract red flags from normalized message text.

Responsibilities:

- Match text patterns against the signal taxonomy
- Return structured detected-signal records
- Include supporting evidence snippets when safe and useful
- Avoid definitive judgments

### Category Classifier

Purpose: Identify the likely scam category when enough context exists.

Responsibilities:

- Classify messages into categories such as delivery, bank alert, marketplace, crypto, job offer, rental, family emergency, or unknown
- Treat category as contextual guidance, not proof
- Return low-confidence or unknown when signals are ambiguous

### Risk Scorer

Purpose: Convert detected signals into a risk level and numeric score.

Responsibilities:

- Combine signal severity and frequency
- Increase risk for high-caution scenarios such as gift cards, crypto, wire transfers, payment apps, and urgent family emergency messages
- Map scores to low, medium, high, or critical risk
- Keep scoring rules deterministic and documented

### Safety Guidance Generator

Purpose: Produce safe, practical next steps.

Responsibilities:

- Recommend verification through official channels
- Warn against clicking suspicious links or sharing sensitive information
- Warn against sending money when payment pressure or irreversible payment methods are present
- Provide stronger caution for high and critical risk
- Explain low-confidence cases without overstating certainty

### Result Formatter

Purpose: Package analysis results into a stable output shape.

Responsibilities:

- Format risk level, score, category, signals, explanation, unsafe actions, safest next step, parent-friendly explanation, and disclaimer
- Use cautious language
- Keep output suitable for future UI rendering
- Keep field names stable for tests and future integrations

## 5. Planned Output Schema

Planned result fields:

```json
{
  "risk_level": "low | medium | high | critical",
  "risk_score": 0,
  "category": "delivery | bank_alert | marketplace | crypto | job_offer | rental | family_emergency | unknown",
  "detected_signals": [],
  "explanation": "",
  "unsafe_actions": [],
  "safest_next_step": "",
  "parent_friendly_explanation": "",
  "disclaimer": ""
}
```

Field definitions:

- `risk_level`: Human-readable risk band using low, medium, high, or critical.
- `risk_score`: Deterministic numeric score used to calculate the risk level.
- `category`: Likely scam category, or unknown when confidence is low.
- `detected_signals`: Structured list of red flags found in the message.
- `explanation`: Plain-language explanation of why the message looks risky.
- `unsafe_actions`: Actions the user should avoid, such as clicking links, sharing OTPs, or sending money.
- `safest_next_step`: The single most useful safety recommendation.
- `parent_friendly_explanation`: Short, non-technical explanation suitable for sharing with a family member.
- `disclaimer`: Clear reminder that ScamSense provides risk guidance, not proof.

## 6. Testing Strategy

### Unit Tests for Signal Detection

Each signal in the taxonomy should have focused tests proving that it triggers for representative fictional examples and does not trigger for unrelated text.

### Unit Tests for Scoring

Risk scoring tests should cover:

- Low, medium, high, and critical outcomes
- Single strong signals
- Multiple weak signals
- High-caution payment scenarios
- Low-confidence or ambiguous inputs

### Fixture-Based Sample Messages

Tests should use fictional sample messages from the project fixture library. Fixtures should cover delivery, bank alert, marketplace, crypto, job offer, rental, family emergency, and benign or ambiguous examples.

### Regression Tests for Known Scam Patterns

When a pattern is added to the taxonomy, a regression test should preserve the expected behavior. This will help prevent future scoring or wording changes from weakening important protections.

## 7. Why Rule-Based First

Rule-based analysis is the right v0.1 foundation because it is:

- Explainable: each result can point back to specific signals and rules.
- Testable: expected behavior can be covered with focused unit tests.
- Deterministic: the same input should produce the same result.
- Safer for v0.1: language, scoring, and privacy behavior are easier to control.

An AI explanation layer may be added later, but the first version should establish a reliable and auditable baseline for scam-risk signals, scoring, guidance, and disclaimers.
