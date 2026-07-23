"""Safety-first explanations derived only from deterministic analysis results."""

from __future__ import annotations

from collections.abc import Sequence

from scamsense.models import CategoryResult, DetectedSignal, RiskResult

DISCLAIMER = (
    "ScamSense is an educational screening aid, not a guarantee. "
    "A lower-risk result does not prove a message is safe, and a high-risk result "
    "does not prove fraud. Verify unexpected requests through official channels."
)

SCAMWATCH_REPORT_URL = "https://portal.scamwatch.gov.au/report-a-scam/"
CYBER_RECOVERY_URL = "https://www.cyber.gov.au/report-and-recover/recover-from/scams"


def build_explanation(risk: RiskResult, signals: Sequence[DetectedSignal]) -> str:
    if not signals:
        return (
            "No obvious indicators were detected in this text. There may be too little "
            "context, so independently verify any unexpected request before acting."
        )
    signal_names = ", ".join(signal.category.casefold() for signal in signals[:3])
    return (
        f"This looks {risk.level.value} risk because the message contains indicators "
        f"including {signal_names}. These are warning signs, not proof."
    )


def build_unsafe_actions(signals: Sequence[DetectedSignal]) -> tuple[str, ...]:
    ids = {signal.id for signal in signals}
    actions: list[str] = []
    if ids & {"suspicious_link", "shortened_url", "institution_impersonation"}:
        actions.append("Do not click links or open unexpected attachments.")
    if ids & {"credentials", "bank_details", "identity_documents", "crypto"}:
        actions.append(
            "Do not disclose passwords, verification codes, financial details or identity documents."
        )
    if ids & {
        "payment_pressure",
        "gift_cards",
        "wire_transfer",
        "crypto",
        "marketplace_manipulation",
        "family_emergency",
    }:
        actions.append("Do not transfer money, crypto, gift cards or codes under pressure.")
    if not actions:
        actions.append(
            "Do not take unexpected action until you have checked the request independently."
        )
    return tuple(actions)


def build_safest_next_step(category: CategoryResult) -> str:
    if category.category.value == "family emergency":
        return (
            "Pause and contact the person through a known existing number, or ask another "
            "trusted family member to verify the story."
        )
    return (
        "Pause and contact the person or organisation using contact details you find "
        "yourself in its official app or website—not details from this message."
    )


def build_parent_friendly_explanation(
    risk: RiskResult,
    signals: Sequence[DetectedSignal],
) -> str:
    if not signals:
        return (
            "We did not find an obvious warning sign in this short check, but that does not "
            "guarantee the message is safe. Use a known number or official app to check it."
        )
    return (
        f"This message looks {risk.level.value} risk because it uses "
        f"{len(signals)} warning sign{'s' if len(signals) != 1 else ''}. "
        "Please pause and check with the person or organisation another way before replying."
    )
