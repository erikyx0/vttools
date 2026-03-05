"""Thermophysical property backend interfaces and service layer."""

from .backend import PropsBackend
from .exceptions import (
    BackendNotAvailableError,
    ConvergenceError,
    OutOfRangeError,
    PhaseAmbiguityError,
    PropsError,
    UnsupportedCapabilityError,
)
from .models import (
    BackendMetadata,
    FlashResult,
    FluidSpec,
    PropertyResult,
    Quantity,
    StatePoint,
)
from .service import PropsService

__all__ = [
    "BackendMetadata",
    "BackendNotAvailableError",
    "ConvergenceError",
    "FlashResult",
    "FluidSpec",
    "OutOfRangeError",
    "PhaseAmbiguityError",
    "PropertyResult",
    "PropsBackend",
    "PropsError",
    "PropsService",
    "Quantity",
    "StatePoint",
    "UnsupportedCapabilityError",
]
