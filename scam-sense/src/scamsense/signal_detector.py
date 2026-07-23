"""Rule-based scam-risk signal detection."""

from __future__ import annotations

import re

from scamsense.models import DetectedSignal
from scamsense.signal_taxonomy import SIGNAL_DEFINITIONS

MAX_INPUT_CHARACTERS = 20_000
MAX_EVIDENCE_CHARACTERS = 80


def normalise_message(message: str) -> str:
    """Normalise whitespace and casing without retaining the message."""
    return " ".join(message[:MAX_INPUT_CHARACTERS].casefold().split())


def detect_signals(message: str) -> tuple[DetectedSignal, ...]:
    """Return each matching signal once, in stable taxonomy order."""
    normalised = normalise_message(message)
    if not normalised:
        return ()

    detected: list[DetectedSignal] = []
    for definition in SIGNAL_DEFINITIONS:
        match = next(
            (
                pattern_match
                for pattern in definition.patterns
                if (pattern_match := re.search(pattern, normalised, flags=re.IGNORECASE))
            ),
            None,
        )
        if match is None:
            continue
        evidence = match.group(0).strip()[:MAX_EVIDENCE_CHARACTERS]
        detected.append(
            DetectedSignal(
                id=definition.id,
                category=definition.category,
                severity=definition.severity,
                description=definition.description,
                why_it_matters=definition.why_it_matters,
                evidence=evidence,
            )
        )
    return tuple(detected)
