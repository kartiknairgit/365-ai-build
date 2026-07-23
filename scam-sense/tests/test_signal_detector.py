from scamsense.models import Severity
from scamsense.sample_messages import SAMPLE_MESSAGES
from scamsense.signal_detector import MAX_INPUT_CHARACTERS, detect_signals, normalise_message
from scamsense.signal_taxonomy import SIGNAL_DEFINITIONS


def ids(message: str) -> set[str]:
    return {signal.id for signal in detect_signals(message)}


def test_empty_and_whitespace_input_returns_no_signals() -> None:
    assert detect_signals("") == ()
    assert detect_signals(" \n\t ") == ()


def test_input_is_normalised_and_bounded() -> None:
    assert normalise_message("  FINAL \n warning  ") == "final warning"
    assert len(normalise_message("x" * (MAX_INPUT_CHARACTERS + 20))) == MAX_INPUT_CHARACTERS


def test_delivery_sample_detects_link_urgency_payment_and_impersonation() -> None:
    assert {
        "suspicious_link",
        "urgency",
        "payment_pressure",
        "institution_impersonation",
    } <= ids(SAMPLE_MESSAGES["Delivery fee"])


def test_bank_sample_detects_credentials() -> None:
    assert {"credentials", "institution_impersonation", "suspicious_link"} <= ids(
        SAMPLE_MESSAGES["Bank verification"]
    )


def test_high_caution_samples_detect_expected_signals() -> None:
    assert "marketplace_manipulation" in ids(SAMPLE_MESSAGES["Marketplace courier"])
    assert {"crypto", "investment_claim"} <= ids(SAMPLE_MESSAGES["Crypto investment"])
    assert {"fake_job", "gift_cards"} <= ids(SAMPLE_MESSAGES["Job offer"])
    assert "rental" in ids(SAMPLE_MESSAGES["Rental deposit"])
    assert {"family_emergency", "secrecy"} <= ids(SAMPLE_MESSAGES["Family emergency"])
    assert "bank_details" in ids(SAMPLE_MESSAGES["Tax refund"])


def test_remaining_taxonomy_signals_have_focused_fictional_examples() -> None:
    examples = {
        "shortened_url": "Open https://bit.ly/example-now",
        "wire_transfer": "Use this new payee for an instant transfer.",
        "identity_documents": "Upload a photo of your passport before the rental viewing.",
    }
    for signal_id, message in examples.items():
        assert signal_id in ids(message)


def test_routine_message_does_not_trigger_risk_signals() -> None:
    assert detect_signals(SAMPLE_MESSAGES["Routine appointment (lower risk)"]) == ()


def test_each_signal_is_structured_and_detected_once() -> None:
    detected = detect_signals("URGENT urgent urgent: act now")
    assert len(detected) == 1
    assert detected[0].id == "urgency"
    assert detected[0].severity is Severity.MEDIUM
    assert detected[0].description
    assert detected[0].why_it_matters
    assert detected[0].evidence


def test_taxonomy_ids_are_unique() -> None:
    taxonomy_ids = [definition.id for definition in SIGNAL_DEFINITIONS]
    assert len(taxonomy_ids) == len(set(taxonomy_ids))
