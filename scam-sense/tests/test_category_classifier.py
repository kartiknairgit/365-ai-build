import pytest

from scamsense.category_classifier import classify_category
from scamsense.models import Confidence, ScamCategory
from scamsense.sample_messages import SAMPLE_MESSAGES


@pytest.mark.parametrize(
    ("sample", "expected"),
    [
        ("Delivery fee", ScamCategory.DELIVERY),
        ("Bank verification", ScamCategory.BANK),
        ("Marketplace courier", ScamCategory.MARKETPLACE),
        ("Crypto investment", ScamCategory.CRYPTO),
        ("Job offer", ScamCategory.JOB),
        ("Rental deposit", ScamCategory.RENTAL),
        ("Family emergency", ScamCategory.FAMILY_EMERGENCY),
        ("Tax refund", ScamCategory.TAX_GOVERNMENT),
    ],
)
def test_fictional_samples_are_classified(sample: str, expected: ScamCategory) -> None:
    result = classify_category(SAMPLE_MESSAGES[sample])
    assert result.category is expected
    assert result.confidence in {Confidence.MEDIUM, Confidence.HIGH}


def test_unknown_is_used_when_context_is_missing() -> None:
    assert (
        classify_category("Hello, are we still meeting tomorrow?").category is ScamCategory.UNKNOWN
    )


def test_one_weak_hint_is_not_treated_as_proof() -> None:
    result = classify_category("Your parcel")
    assert result.category is ScamCategory.UNKNOWN
    assert result.confidence is Confidence.LOW


def test_tied_category_hints_return_unknown() -> None:
    result = classify_category("Bank job")
    assert result.category is ScamCategory.UNKNOWN
