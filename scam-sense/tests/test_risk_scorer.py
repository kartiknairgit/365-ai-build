import pytest

from scamsense.models import DetectedSignal, RiskLevel, Severity
from scamsense.risk_scorer import risk_level_for_score, score_signals
from scamsense.sample_messages import SAMPLE_MESSAGES
from scamsense.signal_detector import detect_signals


def signal(signal_id: str, severity: Severity) -> DetectedSignal:
    return DetectedSignal(signal_id, signal_id, severity, "Description", "Reason", "evidence")


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0, RiskLevel.LOW),
        (19, RiskLevel.LOW),
        (20, RiskLevel.MEDIUM),
        (49, RiskLevel.MEDIUM),
        (50, RiskLevel.HIGH),
        (79, RiskLevel.HIGH),
        (80, RiskLevel.CRITICAL),
        (100, RiskLevel.CRITICAL),
    ],
)
def test_documented_threshold_boundaries(score: int, expected: RiskLevel) -> None:
    assert risk_level_for_score(score) is expected


def test_severity_weights_map_to_expected_levels() -> None:
    assert score_signals([]).score == 0
    assert score_signals([signal("weak", Severity.LOW)]).score == 5
    assert score_signals([signal("context", Severity.MEDIUM)]).score == 15
    assert (
        score_signals([signal("strong_a", Severity.HIGH), signal("strong_b", Severity.HIGH)]).score
        == 60
    )
    assert score_signals([signal("critical", Severity.CRITICAL)]).score == 80


def test_repeated_signal_does_not_inflate_score() -> None:
    repeated = signal("urgency", Severity.MEDIUM)
    assert score_signals([repeated, repeated]).base_score == 15


def test_combined_urgency_and_payment_adds_documented_adjustment() -> None:
    result = score_signals(
        [signal("urgency", Severity.MEDIUM), signal("payment_pressure", Severity.HIGH)]
    )
    assert result.score == 55
    assert result.level is RiskLevel.HIGH
    assert "Urgency plus payment pressure: +10" in result.adjustments


def test_scores_are_capped_at_100() -> None:
    result = score_signals([signal(f"critical_{number}", Severity.CRITICAL) for number in range(3)])
    assert result.score == 100


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        ("Routine appointment (lower risk)", RiskLevel.LOW),
        ("Ambiguous account note", RiskLevel.LOW),
        ("Marketplace courier", RiskLevel.HIGH),
        ("Delivery fee", RiskLevel.CRITICAL),
        ("Bank verification", RiskLevel.CRITICAL),
        ("Crypto investment", RiskLevel.CRITICAL),
        ("Job offer", RiskLevel.CRITICAL),
        ("Family emergency", RiskLevel.CRITICAL),
    ],
)
def test_fictional_samples_have_expected_risk(sample: str, expected: RiskLevel) -> None:
    result = score_signals(detect_signals(SAMPLE_MESSAGES[sample]))
    assert result.level is expected


def test_scoring_contract_contains_no_definitive_language() -> None:
    result = score_signals(detect_signals(SAMPLE_MESSAGES["Bank verification"]))
    rendered = repr(result).casefold()
    assert "definitely scam" not in rendered
    assert "definitely safe" not in rendered
