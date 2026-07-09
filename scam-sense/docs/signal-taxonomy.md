# Signal Taxonomy

## Overview

This document defines the initial ScamSense scam-risk signal taxonomy for Issue #1. It is a planning document for the future v0.1 rule-based MVP and does not implement detection logic.

The taxonomy should help ScamSense explain why a message looks risky without claiming certainty. Each signal represents an observable pattern that may increase scam risk when found in a suspicious SMS, email, marketplace message, job offer, crypto DM, rental message, or urgent family text.

## Signal Object Shape

Planned signal object shape:

```json
{
  "id": "string_identifier",
  "category": "human-readable category",
  "severity": "low | medium | high | critical",
  "description": "What the signal means",
  "why_it_matters": "Why users should treat it carefully",
  "evidence": "Optional short phrase or matched pattern",
  "v0_1_detection_notes": "Rule-based detection guidance"
}
```

The `evidence` field should use only the minimum text needed to explain the signal. ScamSense should avoid storing raw user messages in v0.1.

## Severity Levels

### Low

The signal is weak or contextual. It may be harmless on its own but can contribute to risk when combined with other signals.

### Medium

The signal is meaningfully suspicious and should prompt caution, especially if it involves links, urgency, unusual instructions, or account-related pressure.

### High

The signal indicates a strong risk pattern, such as requests for sensitive information, unusual payment methods, impersonation, or transaction manipulation.

### Critical

The signal involves immediate financial loss, account takeover risk, identity theft risk, irreversible payment pressure, or direct requests for credentials, OTPs, seed phrases, gift card codes, or identity documents.

## Signal Categories

### Suspicious Links

Description: The message asks the user to open a link to resolve an issue, confirm an account, pay a fee, track an item, claim a reward, or continue a transaction.

Why it matters: Scam messages often use links to collect credentials, payment details, personal information, or malware downloads. The displayed sender name may not prove the link is safe.

Fictional example phrases:

- "Confirm your account here: `https://secure-update-example.test`"
- "Pay the redelivery fee at `https://parcel-help-example.test/pay`"
- "View your refund at `https://refund-portal-example.test`"

Suggested severity: High

Notes for v0.1 detection: Detect URL-like patterns, especially when paired with account, payment, delivery, refund, or verification language. Do not attempt live URL reputation checks in v0.1.

### Shortened URLs

Description: The message uses a shortened or obscured URL instead of a clear official domain.

Why it matters: Shortened links can hide the final destination and make it harder for users to inspect whether a link is associated with the claimed sender.

Fictional example phrases:

- "Track it here: `https://short-link-example.test/abc123`"
- "Your secure form: `https://tiny-example.test/paynow`"
- "Open this private link: `https://go-example.test/x9k2`"

Suggested severity: Medium

Notes for v0.1 detection: Maintain a small list of known shortener-like patterns for fictional/test use and detect generic short-link phrasing. Avoid claiming a shortened link is malicious by itself.

### Urgency Pressure

Description: The message pressures the user to act immediately or face a penalty, loss, suspension, missed opportunity, or danger.

Why it matters: Urgency reduces careful thinking and pushes users to click, pay, or share information before verifying independently.

Fictional example phrases:

- "Act within 10 minutes or your account will be locked"
- "Final warning before your delivery is returned"
- "I need this done right now, please do not wait"

Suggested severity: Medium

Notes for v0.1 detection: Detect time-pressure words such as "urgent", "immediately", "final warning", "last chance", "today only", and "right now". Increase severity when combined with payment or credential requests.

### Payment Pressure

Description: The message pushes the user to send money, pay a fee, complete a transfer, or make a payment before normal verification.

Why it matters: Payment pressure is a common scam pattern, especially when the reason is vague, emotional, unexpected, or tied to a threat or promised reward.

Fictional example phrases:

- "Pay this small fee now to release the package"
- "Transfer the amount today so the account stays active"
- "Send the deposit first and I will arrange the pickup"

Suggested severity: High

Notes for v0.1 detection: Detect payment verbs and money terms. Increase risk when paired with urgency, secrecy, links, new payees, or irreversible payment methods.

### Gift Cards

Description: The message asks the user to buy gift cards, prepaid cards, vouchers, or send photos of card codes.

Why it matters: Gift card payments are difficult to reverse and are rarely a legitimate way to pay banks, employers, government agencies, relatives, landlords, or marketplaces.

Fictional example phrases:

- "Buy three gift cards and send the codes"
- "Scratch the voucher and upload a photo"
- "Use prepaid cards for payroll verification"

Suggested severity: Critical

Notes for v0.1 detection: Detect "gift card", "voucher", "prepaid card", "scratch code", and "send the code". Treat as critical when paired with payment, job, family emergency, or government impersonation context.

### Crypto Payments

Description: The message asks for cryptocurrency payment, wallet access, seed phrases, or promises crypto profits.

Why it matters: Crypto transfers are often irreversible, and requests for seed phrases or wallet credentials can lead to immediate asset theft.

Fictional example phrases:

- "Send crypto to this wallet to unlock your return"
- "Share your seed phrase so I can verify the wallet"
- "Guaranteed daily crypto profits if you deposit today"

Suggested severity: Critical

Notes for v0.1 detection: Detect terms such as "crypto", "Bitcoin", "wallet", "seed phrase", "private key", and "guaranteed returns". Seed phrase or private key requests should be critical.

### Wire Transfers

Description: The message instructs the user to send money by wire transfer, bank transfer, or instant transfer to a new or unusual recipient.

Why it matters: Wire transfers and instant bank transfers can be hard to reverse, especially when sent under pressure or to a new payee.

Fictional example phrases:

- "Wire the deposit today to secure the rental"
- "Send an instant bank transfer before pickup"
- "Use this new account because our usual account is unavailable"

Suggested severity: High

Notes for v0.1 detection: Detect "wire", "bank transfer", "instant transfer", "new account", and "new payee". Increase risk when paired with urgency, rental, job, marketplace, or family emergency language.

### OTP/Password Requests

Description: The message asks for passwords, one-time passcodes, login codes, recovery codes, or authentication details.

Why it matters: Legitimate organizations generally do not ask users to reveal passwords or OTPs in messages. Sharing them can allow account takeover.

Fictional example phrases:

- "Send the one-time code so we can verify you"
- "Reply with your password to unlock the account"
- "Tell me the recovery code from your app"

Suggested severity: Critical

Notes for v0.1 detection: Detect "OTP", "one-time code", "verification code", "password", "recovery code", "login code", and similar phrases. Treat direct requests to share these values as critical.

### Bank/Card Detail Requests

Description: The message requests card numbers, bank login details, account numbers, PINs, CVV codes, or payment details.

Why it matters: These details can be used for unauthorized transactions, account takeover, or identity fraud.

Fictional example phrases:

- "Confirm your card number and CVV"
- "Reply with your online banking login"
- "Enter your account details to receive the refund"

Suggested severity: Critical

Notes for v0.1 detection: Detect card, CVV, PIN, account number, bank login, and refund-confirmation patterns. Increase risk when linked to bank impersonation or suspicious links.

### Identity Document Requests

Description: The message asks for identity documents such as a passport, driver's licence, national ID, selfie, or proof of address.

Why it matters: Identity documents can be used for identity theft, account opening, SIM swap attempts, or financial fraud.

Fictional example phrases:

- "Send a photo of your passport to confirm the job"
- "Upload your driver's licence before viewing the rental"
- "Send a selfie holding your ID for payment release"

Suggested severity: Critical

Notes for v0.1 detection: Detect document names and upload/send-photo phrasing. Treat requests as high or critical depending on whether they are paired with job, rental, payment, or account-verification pressure.

### Impersonation of Banks/Government/Delivery Services

Description: The message claims to be from a bank, government agency, tax office, delivery provider, postal service, or other trusted institution.

Why it matters: Impersonation borrows trust from familiar institutions to make users click links, share details, or make payments.

Fictional example phrases:

- "Your bank account has been locked"
- "Government refund pending verification"
- "Delivery service: your parcel is on hold"

Suggested severity: High

Notes for v0.1 detection: Detect institution-like terms and account, refund, tax, delivery, or verification phrasing. Avoid trying to verify real brand identity in v0.1.

### Marketplace Payment Manipulation

Description: The message tries to move payment, shipping, pickup, insurance, or buyer/seller protection outside normal marketplace processes.

Why it matters: Scammers often manipulate marketplace workflows to make users pay fees, leave platform protections, or trust fake courier/payment confirmations.

Fictional example phrases:

- "The courier needs you to pay refundable insurance first"
- "I already paid, check this outside payment link"
- "Leave the marketplace chat so I can arrange pickup"

Suggested severity: High

Notes for v0.1 detection: Detect courier, insurance, refundable fee, outside payment, pickup arrangement, and off-platform messaging phrases. Increase risk when the seller is asked to pay to receive money.

### Fake Job Offer Signals

Description: The message describes a job offer with unusual hiring steps, unrealistic pay, no interview, upfront payments, gift cards, or equipment/payment handling.

Why it matters: Fake job scams can lead to financial loss, identity theft, or money-mule activity.

Fictional example phrases:

- "No interview required for this high-paying remote role"
- "Buy equipment first and we will reimburse you"
- "Send gift card codes to activate payroll"

Suggested severity: High

Notes for v0.1 detection: Detect job-offer terms paired with unrealistic pay, no interview, upfront fees, reimbursement, payroll verification, gift cards, or equipment purchase requests.

### Rental Scam Signals

Description: The message asks for deposits, identity documents, or fees before a viewing, lease verification, or independent confirmation.

Why it matters: Rental scams often pressure users to pay quickly for properties they have not inspected or to share identity documents before legitimacy is established.

Fictional example phrases:

- "Send the bond today before viewing"
- "The rent is far below market because I moved overseas"
- "Upload your ID and deposit to reserve the apartment"

Suggested severity: High

Notes for v0.1 detection: Detect rental terms paired with deposit, bond, urgent reservation, below-market rent, overseas owner, ID upload, or viewing avoidance.

### Family Emergency Manipulation

Description: The message claims to be a family member or friend in urgent trouble and asks for immediate money, secrecy, or no phone call.

Why it matters: Emotional pressure can cause users to bypass normal verification, especially when the message claims a new number or asks them not to call.

Fictional example phrases:

- "Mum, this is my new number and I need money now"
- "Please do not call, just transfer it quickly"
- "I am in trouble and cannot explain until later"

Suggested severity: Critical

Notes for v0.1 detection: Detect family terms, new-number claims, urgent money requests, "do not call", secrecy, and emergency language. Recommend contacting the person through a known existing number.

### Too-Good-To-Be-True Investment Claims

Description: The message promises unusually high, guaranteed, or fast returns from an investment, trading system, crypto opportunity, or limited offer.

Why it matters: Guaranteed profit claims and unrealistic returns are strong scam-risk patterns, especially when paired with urgency or a request to deposit funds.

Fictional example phrases:

- "Guaranteed 10x return by next week"
- "Turn $300 into $3,000 with no risk"
- "Limited investment spots, deposit today"

Suggested severity: High

Notes for v0.1 detection: Detect "guaranteed returns", "no risk", "double your money", "10x", "limited spots", and fast-profit claims. Increase risk when paired with crypto, payment links, or urgency.
