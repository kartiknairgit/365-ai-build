# Risk Scoring Model

## Overview

This document defines the planned v0.1 rule-based risk scoring model for ScamSense. It is design documentation only and does not implement scoring logic.

The model should convert detected scam-risk signals into a transparent risk level. It should explain why a message looks risky, recommend safe next steps, and avoid definitive claims about whether a message is fraudulent or safe.

The v0.1 scoring model should be:

- Explainable: every score should map back to detected signals.
- Deterministic: the same input and signals should produce the same score.
- Conservative: uncertainty should lead to verification guidance, not reassurance.
- Testable: thresholds, weights, and escalation rules should be easy to cover with future pytest tests.

## Risk Score Range

The planned score range is `0` to `100`.

- `0` means no meaningful scam-risk signals were detected.
- `100` means the message contains critical risk patterns such as credential requests, OTP requests, gift card codes, seed phrases, or urgent irreversible payment pressure.

The score is guidance only. A low score does not prove a message is safe, and a high score does not prove a message is fraudulent.

## Risk Levels

### Low

The message has few or weak risk signals. It may still need verification if it asks the user to click a link, share information, send money, or take account-related action.

Recommended wording:

> This looks low risk based on the signals detected, but verify through official channels before acting.

### Medium

The message contains meaningful scam-risk signals, such as urgency, vague sender identity, suspicious links, or pressure to act quickly.

Recommended wording:

> This looks medium risk because it contains scam-risk signals such as urgency or a suspicious link.

### High

The message contains strong scam-risk signals, such as payment pressure, impersonation, marketplace manipulation, identity-document requests, fake job-offer patterns, or investment claims.

Recommended wording:

> This looks high risk because it asks for sensitive action or uses patterns commonly seen in scams.

### Critical

The message contains immediate user-protection risks, such as requests for OTPs, passwords, card details, gift card codes, crypto seed phrases, or urgent irreversible payments.

Recommended wording:

> This looks critical risk because it asks for information or payment that could cause immediate account, identity, or financial harm.

## Suggested Numeric Thresholds

Planned thresholds:

- `0-19`: Low
- `20-49`: Medium
- `50-79`: High
- `80-100`: Critical

These thresholds should be treated as initial v0.1 defaults. Future testing may adjust them if sample messages produce risk levels that do not match the intended safety posture.

## How Detected Scam Signals Contribute to Score

Each detected signal should contribute points based on severity. Signals should also include category information so the explanation can describe the risk in plain language.

Signals may contribute through:

- Base severity weight
- Category-specific escalation
- Combined-signal escalation
- Critical override rules
- Confidence adjustment

The score should be capped at `100`.

## Severity Weighting Model

Suggested base weights:

| Signal severity | Base score |
| --- | ---: |
| Low | 5 |
| Medium | 15 |
| High | 30 |
| Critical | 60 |

Suggested handling:

- Multiple low signals may combine into medium risk.
- A single high signal should usually produce at least high-end medium or high risk.
- A single critical signal should usually produce critical risk or near-critical risk.
- Repeated signals in the same category should not inflate the score without limit.

## Examples of Scoring

All examples are fictional.

### Fake Delivery Fee SMS

Fictional message:

> Your parcel could not be delivered. Pay the $2.14 redelivery fee now at `https://parcel-help-example.test/pay` or it will be returned.

Detected signals:

- Suspicious link: high, `30`
- Payment pressure: high, `30`
- Urgency pressure: medium, `15`
- Delivery-service impersonation context: high, `30`

Combined-signal adjustment:

- Link plus payment plus urgency: `+10`

Suggested score: `100`, capped from `115`

Suggested level: Critical

Reasoning: The message combines a link, payment request, urgency, and delivery impersonation context.

### Fake Bank Alert

Fictional message:

> Security alert: your account is locked. Confirm your login and one-time code immediately at `https://secure-bank-example.test`.

Detected signals:

- Bank impersonation context: high, `30`
- Suspicious link: high, `30`
- OTP/password request: critical, `60`
- Urgency pressure: medium, `15`

Combined-signal adjustment:

- Credential or OTP request plus bank context: `+15`

Suggested score: `100`, capped from `150`

Suggested level: Critical

Reasoning: Requests for OTPs or credentials should trigger the strongest safety posture.

### Marketplace Courier Fee

Fictional message:

> I will buy the item today. The courier needs you to pay a refundable insurance fee first through this payment link.

Detected signals:

- Marketplace payment manipulation: high, `30`
- Payment pressure: high, `30`
- Suspicious link: high, `30`
- Urgency pressure: medium, `15`

Combined-signal adjustment:

- Marketplace context plus seller asked to pay a fee: `+10`

Suggested score: `100`, capped from `115`

Suggested level: Critical

Reasoning: The message asks the seller to pay a fee through an unusual marketplace workflow.

### Ambiguous Routine Reminder

Fictional message:

> Reminder: your appointment is tomorrow at 3 pm. Please check your usual account portal for details.

Detected signals:

- No direct payment request
- No sensitive-information request
- No suspicious link in the message
- Mild account-portal reference: low, `5`

Combined-signal adjustment: none

Suggested score: `5`

Suggested level: Low

Reasoning: The message does not contain strong scam-risk signals, but the user should still use the official portal rather than links from unexpected messages.

## Rules for Combined Signals Increasing Risk

Certain combinations should increase the score because they are more dangerous together than alone:

- Suspicious link plus credential, OTP, card, or bank-detail request: add `15` and consider critical.
- Urgency plus payment pressure: add `10`.
- Impersonation plus link: add `10`.
- Impersonation plus credential or OTP request: add `15` and consider critical.
- Marketplace context plus off-platform payment or courier fee: add `10`.
- Job offer plus gift card, upfront payment, or identity-document request: add `15`.
- Rental context plus deposit before viewing or identity-document request: add `10`.
- Family emergency plus money request plus "do not call" instruction: add `15` and consider critical.
- Crypto payment plus guaranteed returns: add `15`.

Combined-signal adjustments should be documented and tested. They should not silently create unexplained score changes.

## Rules for Confidence and Uncertainty

ScamSense should separate risk level from confidence where possible.

Low confidence may occur when:

- The message is very short.
- The message is only a fragment.
- The message has vague language without enough context.
- The message contains one weak signal but no clear requested action.
- The message appears routine but references an account, delivery, payment, or identity process.

Planned confidence values:

- `low`
- `medium`
- `high`

Low confidence should not automatically mean low risk. If the message includes a sensitive action, the result should still recommend verification through official channels.

Suggested behavior:

- Low score plus low confidence: "This looks low risk from the limited text, but there is not enough context to be sure. Verify through official channels before acting."
- Medium or high score plus low confidence: "This looks risky based on the signals present, but the message lacks context. Do not click links or send money until you verify independently."
- Critical signal plus any confidence level: prioritize user protection and recommend stopping before acting.

## Language Constraints

ScamSense must avoid:

- "Definitely scam"
- "Definitely safe"
- "This is fraud"
- "This is legitimate"
- "You can trust this"
- "This link is safe"

ScamSense should use:

- "This looks low risk because..."
- "This looks medium risk because..."
- "This looks high risk because..."
- "This looks critical risk because..."
- "Verify through official channels before acting."
- "Do not click links, share sensitive information, or send money until you have verified independently."

The model should always explain the risk level using detected signals rather than unsupported certainty.

## Safety-First Fallback When Uncertain

When the model is uncertain, the fallback should be practical caution:

- Do not click suspicious links.
- Do not share passwords, OTPs, bank details, card details, or identity documents.
- Do not send money or gift card codes.
- Contact the person or organization through a known official channel.
- Use the official app or website by navigating there directly.
- Ask a trusted person for help before acting if money, identity, or account access is involved.

The fallback should not frighten the user or claim proof. It should slow the user down and guide them toward safer verification.

## Connection to the Signal Taxonomy

The scoring model depends on `signal-taxonomy.md` as the source of planned signal definitions.

The signal taxonomy should define:

- Signal category
- Signal description
- Why the signal matters
- Suggested severity
- v0.1 detection notes

The scoring model should use those severities as inputs, then apply thresholds and combined-signal rules to produce:

- `risk_score`
- `risk_level`
- `explanation`
- `unsafe_actions`
- `safest_next_step`
- `parent_friendly_explanation`
- `disclaimer`

Changes to signal severity in the taxonomy should trigger a review of scoring thresholds and tests.

## Testing Expectations for Future Pytest Implementation

Future pytest coverage should include:

- Unit tests for each risk threshold.
- Unit tests for each severity weight.
- Unit tests for score caps at `100`.
- Unit tests for repeated signals not inflating without limit.
- Unit tests for combined-signal escalation rules.
- Unit tests for critical override behavior.
- Unit tests for low-confidence behavior.
- Unit tests using fictional fixture messages only.
- Regression tests for known scam patterns.
- Tests confirming output avoids "definitely scam" and "definitely safe" language.
- Tests confirming safety-first fallback guidance appears when confidence is low.

Tests should be readable enough to document the expected safety behavior of the scoring model.
