"""Typed contracts shared by the ScamSense analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ScamCategory(StrEnum):
    DELIVERY = "delivery"
    BANK = "bank"
    MARKETPLACE = "marketplace"
    CRYPTO = "crypto"
    JOB = "job"
    RENTAL = "rental"
    FAMILY_EMERGENCY = "family emergency"
    TAX_GOVERNMENT = "tax or government"
    UNKNOWN = "unknown"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class SignalDefinition:
    id: str
    category: str
    severity: Severity
    description: str
    why_it_matters: str
    patterns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DetectedSignal:
    id: str
    category: str
    severity: Severity
    description: str
    why_it_matters: str
    evidence: str


@dataclass(frozen=True, slots=True)
class CategoryResult:
    category: ScamCategory
    confidence: Confidence
    matched_hints: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RiskResult:
    score: int
    level: RiskLevel
    base_score: int
    adjustments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    risk: RiskResult
    category: CategoryResult
    detected_signals: tuple[DetectedSignal, ...]
    explanation: str
    unsafe_actions: tuple[str, ...]
    safest_next_step: str
    parent_friendly_explanation: str
    disclaimer: str
