# ScamSense

ScamSense is an explainable scam-risk assistant for suspicious messages.

Users paste a suspicious SMS, email, marketplace message, job offer, crypto DM, rental message, or urgent family text. ScamSense identifies scam risk signals, explains why those signals matter, and suggests the safest next step.

## Problem

Scams increasingly arrive through everyday communication channels: text messages, email, social media DMs, marketplace chats, job offers, rental listings, and family emergency messages. Many people can sense that something feels wrong, but they may not know which details matter or how to verify the message safely.

Existing scam-detection tools can be useful, but many focus on quick verdicts. A simple "scam" or "not scam" label can leave users without enough context to make a careful decision.

## Solution

ScamSense focuses on transparent reasoning. Instead of claiming certainty, it highlights observable risk signals such as urgency, payment pressure, impersonation, suspicious links, requests for sensitive information, or unusual financial instructions.

The goal is to help users pause, understand the risk, and verify through official channels before taking action.

## Planned MVP

The first version will be a rule-based prototype that accepts pasted message text and returns:

- A low, medium, or high scam-risk level
- A short explanation of triggered risk signals
- A plain-language summary suitable for non-technical users
- Safety-first next steps, such as verifying independently or avoiding links and payments
- A disclaimer that the result is guidance, not a definitive determination

## Planned Tech Stack

- Python for core analysis logic
- Pytest for automated tests
- Streamlit for a future demo interface
- Optional AI explanation layer in a later version

No app interface or external API integration is included in this initial setup.

## Product Philosophy

ScamSense is designed around four principles:

- Be explainable before being clever.
- Use cautious, non-definitive language.
- Make guidance family-friendly and easy to share.
- Recommend verification through official channels before any action.

ScamSense should not say, "this is definitely a scam." It should say, "this looks low, medium, or high risk because of these signals. Verify through official channels before acting."

## Disclaimer

ScamSense is an educational and decision-support tool. It does not provide legal, financial, banking, cybersecurity, or law-enforcement advice. A low-risk result does not guarantee that a message is safe, and a high-risk result does not prove fraud. Users should verify suspicious messages through official channels and contact relevant institutions or authorities when appropriate.
