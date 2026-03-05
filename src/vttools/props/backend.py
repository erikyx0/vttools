"""Backend protocol for thermophysical property engines."""

from __future__ import annotations

from typing import Protocol

from .models import FlashResult, FluidSpec, PropertyResult, Quantity, StatePoint


class PropsBackend(Protocol):
    """Contract adapters (CoolProp, REFPROP, ...) should implement."""

    name: str

    def capabilities(self) -> set[str]:
        """Return available capability identifiers."""

    def metadata(self) -> dict[str, str]:
        """Return backend/data version metadata."""

    def get_property(
        self,
        property_name: str,
        state: StatePoint,
        fluid: FluidSpec,
    ) -> PropertyResult:
        """Return a single property at a given state."""

    def get_derivative(
        self,
        property_name: str,
        wrt: str,
        constant: str,
        state: StatePoint,
        fluid: FluidSpec,
    ) -> PropertyResult:
        """Return a derivative, e.g. (dh/dT)_p."""

    def flash(
        self,
        flash_spec: str,
        values: dict[str, Quantity],
        fluid: FluidSpec,
    ) -> FlashResult:
        """Solve a flash problem such as TP/PH/PS/PQ."""
