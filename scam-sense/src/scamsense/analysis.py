"""Stable analysis entry point that composes detection, classification and scoring."""

from scamsense.category_classifier import classify_category
from scamsense.guidance import (
    DISCLAIMER,
    build_explanation,
    build_parent_friendly_explanation,
    build_safest_next_step,
    build_unsafe_actions,
)
from scamsense.models import AnalysisResult
from scamsense.risk_scorer import score_signals
from scamsense.signal_detector import detect_signals


def analyse_message(message: str) -> AnalysisResult:
    signals = detect_signals(message)
    category = classify_category(message)
    risk = score_signals(signals)
    return AnalysisResult(
        risk=risk,
        category=category,
        detected_signals=signals,
        explanation=build_explanation(risk, signals),
        unsafe_actions=build_unsafe_actions(signals),
        safest_next_step=build_safest_next_step(category),
        parent_friendly_explanation=build_parent_friendly_explanation(risk, signals),
        disclaimer=DISCLAIMER,
    )
