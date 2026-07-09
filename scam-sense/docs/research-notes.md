# Research Notes

## Current Solution Landscape

Scam-prevention support already exists across several categories. Many tools and organizations help users identify, report, or learn about scams. ScamSense should complement this landscape rather than claim to replace it.

## Existing Categories of Tools

### AI Scam Checkers

Some products let users paste suspicious text, upload screenshots, or check links for potential scam signals. These tools are useful for quick review, but they may provide limited explanation or overly confident labels.

Common capabilities include:

- Message or email classification
- Suspicious-link warnings
- Phishing pattern detection
- Browser or inbox security integrations
- General scam education

### Government Scam Reporting Sites

Government and consumer-protection agencies often provide scam education, reporting forms, and examples of current scam campaigns. These sites are important because they can route users toward official advice and law-enforcement or consumer-protection workflows.

Common capabilities include:

- Scam reporting
- Consumer alerts
- Guidance for victims
- Advice on recovering accounts or limiting financial damage
- Public education about known scam types

### Bank and Security Guidance

Banks, payment providers, cybersecurity companies, and identity-protection services publish guidance on phishing, account takeover, suspicious payments, and safe verification practices.

Common capabilities include:

- Warnings about payment and account scams
- Advice to avoid sharing one-time passcodes or passwords
- Guidance for contacting the institution through official channels
- Fraud response steps for customers
- Account security recommendations

## Opportunity and Gap

The opportunity for ScamSense is not simply detection. The more valuable gap is understandable reasoning.

Users often need help answering:

- What specifically looks risky in this message?
- Why does that detail matter?
- What should I do next without making the situation worse?
- How can I explain this to a family member?

ScamSense can focus on clear explanations, careful uncertainty, and practical next steps. The product can be especially useful when a user is under pressure and needs to slow down before clicking a link, sending money, sharing information, or continuing a conversation.

## Why Rule-Based First Is Safer for v0.1

A rule-based first version is safer and more appropriate for v0.1 because it makes the system behavior easier to inspect, test, and explain.

Benefits of a rule-based approach:

- Transparent logic: each risk signal can be traced to a specific rule.
- Predictable output: similar messages should produce consistent explanations.
- Easier testing: scoring and triggered signals can be covered with focused unit tests.
- Safer language control: the product can consistently avoid definitive claims.
- No external data exposure: pasted user messages do not need to be sent to a third-party API in v0.1.

An AI explanation layer may be useful later, but the first version should establish a clear baseline for risk signals, scoring, disclaimers, and safe next-step guidance.
