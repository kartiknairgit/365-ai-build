"""Context classifier kept separate from signal detection and scoring."""

from __future__ import annotations

import re

from scamsense.models import CategoryResult, Confidence, ScamCategory
from scamsense.signal_detector import normalise_message

CATEGORY_HINTS: dict[ScamCategory, tuple[str, ...]] = {
    ScamCategory.DELIVERY: (r"\bparcel\b", r"\bdelivery\b", r"\bcourier\b", r"\bshipping\b"),
    ScamCategory.BANK: (
        r"\bbank\b",
        r"\bcard\b",
        r"\bonline banking\b",
        r"\baccount (?:has been )?locked\b",
    ),
    ScamCategory.MARKETPLACE: (
        r"\bmarketplace\b",
        r"\bbuyer\b",
        r"\bseller\b",
        r"\bbuy\b",
        r"\bpickup\b",
        r"\bcourier\b",
    ),
    ScamCategory.CRYPTO: (
        r"\bcrypto(?:currency)?\b",
        r"\bbitcoin\b",
        r"\bwallet\b",
        r"\bseed phrase\b",
    ),
    ScamCategory.JOB: (r"\bjob\b", r"\brole\b", r"\brecruiter\b", r"\bpayroll\b", r"\binterview\b"),
    ScamCategory.RENTAL: (
        r"\brent(?:al)?\b",
        r"\bproperty\b",
        r"\bapartment\b",
        r"\blandlord\b",
        r"\bbond\b",
    ),
    ScamCategory.FAMILY_EMERGENCY: (
        r"\bmum\b",
        r"\bmom\b",
        r"\bdad\b",
        r"\bson\b",
        r"\bdaughter\b",
        r"\bnew number\b",
        r"\btemporary number\b",
        r"\bin trouble\b",
        r"\bfamily\b",
    ),
    ScamCategory.TAX_GOVERNMENT: (
        r"\bgovernment\b",
        r"\btax(?:ation)?\b",
        r"\bato\b",
        r"\bmygov\b",
        r"\bfine\b",
    ),
}


def classify_category(message: str) -> CategoryResult:
    normalised = normalise_message(message)
    scores: dict[ScamCategory, list[str]] = {}
    for category, patterns in CATEGORY_HINTS.items():
        matches = [pattern for pattern in patterns if re.search(pattern, normalised)]
        if matches:
            scores[category] = matches

    if not scores:
        return CategoryResult(ScamCategory.UNKNOWN, Confidence.LOW, ())

    ranked = sorted(scores.items(), key=lambda item: (-len(item[1]), item[0].value))
    winner, hints = ranked[0]
    runner_up_score = len(ranked[1][1]) if len(ranked) > 1 else 0
    if len(hints) == 1 or len(hints) == runner_up_score:
        return CategoryResult(ScamCategory.UNKNOWN, Confidence.LOW, tuple(hints))

    confidence = Confidence.HIGH if len(hints) >= 3 else Confidence.MEDIUM
    return CategoryResult(winner, confidence, tuple(hints))
