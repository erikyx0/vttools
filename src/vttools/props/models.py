"""Core data models for thermophysical property workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Quantity:
    """A scalar value with a unit.

    Notes
    -----
    The props core keeps units explicit at API boundaries so a future unit system
    (e.g. Pint integration) can be attached without changing user-facing structs.
    """

    value: float
    unit: str


@dataclass(frozen=True, slots=True)
class StatePoint:
    """Input state definition used for property and flash calculations."""

    inputs: dict[str, Quantity]
    phase_hint: str | None = None


@dataclass(frozen=True, slots=True)
class FluidSpec:
    """Fluid identity and optional mixture composition."""

    name: str
    composition: dict[str, float] | None = None
    basis: str = "mole_fraction"


@dataclass(frozen=True, slots=True)
class BackendMetadata:
    """Provenance info for reproducible calculations."""

    backend: str
    backend_version: str | None = None
    data_version: str | None = None
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PropertyResult:
    """A calculated property with metadata and quality signals."""

    name: str
    quantity: Quantity
    metadata: BackendMetadata
    quality_flags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FlashResult:
    """Container for flash outputs and phase information."""

    state: dict[str, Quantity]
    phase: str
    metadata: BackendMetadata
    quality_flags: tuple[str, ...] = ()
