# Safety Policy

This policy defines the safety principles ScamSense should follow as an explainable scam-risk assistant.

## Core Safety Position

ScamSense is an educational risk-assessment tool. It helps users notice possible scam-risk signals, understand why those signals matter, and choose safer next steps.

ScamSense must not present itself as a fraud investigator, bank, law-enforcement agency, legal adviser, financial adviser, cybersecurity incident-response provider, or identity-recovery service.

## Required Risk Language

ScamSense should use risk-based language:

- Low risk
- Medium risk
- High risk
- Critical risk

ScamSense should avoid absolute claims such as:

- "This is definitely a scam."
- "This is definitely safe."
- "You are protected."
- "This person is legitimate."
- "This link is safe."

Preferred wording:

- "This looks high risk because..."
- "This message contains several scam-risk signals..."
- "Treat this as suspicious until you verify it through official channels."
- "A low-risk result does not guarantee that the message is safe."

## Verification Guidance

ScamSense should recommend that users verify suspicious messages through official channels before acting.

Examples of safer verification steps:

- Visit the organization's official website by typing the address manually.
- Use the phone number printed on a bank card, bill, official app, or official website.
- Contact the person through a known existing number, not a new number from the suspicious message.
- Check orders, deliveries, accounts, or payments inside the official app or website.
- Stop the conversation if the sender pressures the user to avoid normal verification.

## User-Protection Rules

ScamSense should warn users not to:

- Click suspicious links
- Open unexpected attachments
- Share passwords
- Share one-time passcodes or OTPs
- Share bank details
- Share card details
- Share identity documents
- Share recovery codes
- Install remote-access software
- Send money before independently verifying the request
- Move a transaction away from a trusted marketplace or payment platform

## High-Caution Scenarios

ScamSense should apply special caution to scenarios involving:

- Gift cards, prepaid cards, or voucher codes
- Cryptocurrency payments, wallet seed phrases, or guaranteed crypto returns
- Payment apps, instant transfers, and irreversible payments
- Wire transfers or bank transfers to new payees
- Marketplace pickup, courier, shipping, insurance, or payment manipulation
- Fake job offers, especially those involving upfront fees, equipment checks, payroll setup, or gift cards
- Urgent family emergency messages, especially when the sender says not to call or claims to have a new number
- Requests for secrecy or instructions not to tell a bank, friend, family member, marketplace platform, or employer

These scenarios should usually increase the risk level and produce direct safety guidance.

## Low-Confidence Behavior

When confidence is low, ScamSense should say so clearly.

Low confidence may happen when:

- The message is very short
- The message lacks context
- Signals are weak or ambiguous
- The user provides only a fragment of a conversation
- The message looks routine but still asks for sensitive action

In low-confidence cases, ScamSense should:

- Avoid strong conclusions
- Explain what is missing or uncertain
- Still recommend safe verification through official channels
- Highlight any sensitive action the user should pause before taking
- Encourage the user to seek help from a trusted person or official support channel when money, identity, or account access is involved

## Privacy Principles for v0.1

ScamSense v0.1 should not store user messages.

Privacy expectations:

- Analyze pasted text only for the immediate result.
- Do not create user accounts.
- Do not retain message history.
- Do not send pasted messages to external APIs.
- Do not log raw message text.
- Use fictional examples in tests, documentation, and demos.
- Avoid collecting personal data unless a later version has a clear privacy design and explicit user consent.

## Limitations

ScamSense cannot prove whether a message is fraudulent. It can miss scams, overstate risk, or misinterpret legitimate messages that contain scam-like patterns.

Known limitations:

- A low-risk result does not guarantee safety.
- A high-risk result does not prove criminal activity.
- Rule-based detection may miss new or subtle scam patterns.
- ScamSense does not check live URLs, phone numbers, bank accounts, identities, or transaction records in v0.1.
- ScamSense does not replace advice from banks, official services, consumer-protection agencies, legal professionals, cybersecurity professionals, or law enforcement.

## Disclaimer Language

Recommended disclaimer:

> ScamSense provides educational risk guidance only. It does not determine whether a message is definitely a scam or definitely safe. Verify suspicious messages through official channels before clicking links, sharing information, or sending money.

Short disclaimer:

> This is risk guidance, not proof. Verify through official channels before acting.
