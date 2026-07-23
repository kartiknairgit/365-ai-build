import pytest

from scamsense.analysis import analyse_message
from scamsense.models import RiskLevel, ScamCategory
from scamsense.sample_messages import SAMPLE_MESSAGES


@pytest.mark.parametrize(
    "sample",
    [
        "Routine appointment (lower risk)",
        "Ambiguous account note",
        "Delivery fee",
        "Bank verification",
        "Marketplace courier",
        "Crypto investment",
        "Job offer",
        "Rental deposit",
        "Family emergency",
        "Tax refund",
    ],
)
def test_analysis_contract_is_complete_and_cautious(sample: str) -> None:
    result = analyse_message(SAMPLE_MESSAGES[sample])
    assert result.explanation
    assert result.unsafe_actions
    assert result.safest_next_step
    assert result.parent_friendly_explanation
    assert result.disclaimer
    combined = " ".join(
        [
            result.explanation,
            result.safest_next_step,
            result.parent_friendly_explanation,
            result.disclaimer,
        ]
    ).casefold()
    assert "definitely a scam" not in combined
    assert "definitely safe" not in combined
    assert "official" in combined


def test_lower_risk_state_still_warns_about_uncertainty() -> None:
    result = analyse_message(SAMPLE_MESSAGES["Routine appointment (lower risk)"])
    assert result.risk.level is RiskLevel.LOW
    assert result.detected_signals == ()
    assert "does not guarantee" in result.parent_friendly_explanation


def test_family_guidance_uses_known_contact_path() -> None:
    result = analyse_message(SAMPLE_MESSAGES["Family emergency"])
    assert result.category.category is ScamCategory.FAMILY_EMERGENCY
    assert "known existing number" in result.safest_next_step


def test_sensitive_request_produces_specific_unsafe_actions() -> None:
    result = analyse_message(SAMPLE_MESSAGES["Bank verification"])
    joined = " ".join(result.unsafe_actions)
    assert "verification codes" in joined
    assert "click links" in joined
