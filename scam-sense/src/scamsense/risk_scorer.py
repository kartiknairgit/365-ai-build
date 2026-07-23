"""Deterministic signal weighting, combined-signal rules and thresholds."""

from __future__ import annotations

from collections.abc import Iterable

from scamsense.models import DetectedSignal, RiskLevel, RiskResult, Severity

SEVERITY_WEIGHTS = {
    Severity.LOW: 5,
    Severity.MEDIUM: 15,
    Severity.HIGH: 30,
    Severity.CRITICAL: 60,
}


def risk_level_for_score(score: int) -> RiskLevel:
    if score >= 80:
        return RiskLevel.CRITICAL
    if score >= 50:
        return RiskLevel.HIGH
    if score >= 20:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def score_signals(signals: Iterable[DetectedSignal]) -> RiskResult:
    unique = {signal.id: signal for signal in signals}
    ids = set(unique)
    base_score = sum(SEVERITY_WEIGHTS[signal.severity] for signal in unique.values())
    adjustment_points = 0
    adjustments: list[str] = []

    def add(points: int, explanation: str) -> None:
        nonlocal adjustment_points
        adjustment_points += points
        adjustments.append(explanation)

    sensitive = {"credentials", "bank_details", "identity_documents"}
    if "suspicious_link" in ids and ids & sensitive:
        add(15, "Link plus sensitive-information request: +15")
    if {"urgency", "payment_pressure"} <= ids:
        add(10, "Urgency plus payment pressure: +10")
    if {"institution_impersonation", "suspicious_link"} <= ids:
        add(10, "Organisation impersonation plus link: +10")
    if "institution_impersonation" in ids and ids & {"credentials", "bank_details"}:
        add(15, "Organisation impersonation plus account details: +15")
    if {"marketplace_manipulation", "payment_pressure"} <= ids:
        add(10, "Marketplace manipulation plus payment request: +10")
    if "fake_job" in ids and ids & {"gift_cards", "payment_pressure", "identity_documents"}:
        add(15, "Job offer plus payment or identity request: +15")
    if "rental" in ids and ids & {"payment_pressure", "identity_documents"}:
        add(10, "Rental context plus deposit or identity request: +10")
    if {"family_emergency", "payment_pressure", "secrecy"} <= ids:
        add(15, "Family emergency plus payment and no-call pressure: +15")
    if {"crypto", "investment_claim"} <= ids:
        add(15, "Crypto context plus guaranteed-return claim: +15")

    score = min(100, base_score + adjustment_points)
    if any(signal.severity is Severity.CRITICAL for signal in unique.values()):
        score = max(80, score)
        if score > base_score + adjustment_points:
            adjustments.append("Critical user-protection signal: minimum score 80")

    return RiskResult(
        score=score,
        level=risk_level_for_score(score),
        base_score=base_score,
        adjustments=tuple(adjustments),
    )
