"""Deterministic exceptions for props backends."""


class PropsError(Exception):
    """Base exception for props module."""


class BackendNotAvailableError(PropsError):
    """Raised when the requested backend is unknown or unavailable."""


class UnsupportedCapabilityError(PropsError):
    """Raised when a backend does not support a requested operation."""


class OutOfRangeError(PropsError):
    """Raised when an input is outside a model validity range."""


class ConvergenceError(PropsError):
    """Raised when iterative backend routines fail to converge."""


class PhaseAmbiguityError(PropsError):
    """Raised when the state cannot be mapped to a unique phase."""
