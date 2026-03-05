from __future__ import annotations

from dataclasses import dataclass

import pytest

from vttools.props.exceptions import BackendNotAvailableError, UnsupportedCapabilityError
from vttools.props.models import BackendMetadata, FlashResult, FluidSpec, PropertyResult, Quantity, StatePoint
from vttools.props.service import PropsService


@dataclass(slots=True)
class DummyBackend:
    name: str = "dummy"

    def capabilities(self) -> set[str]:
        return {"properties", "derivatives", "flash"}

    def metadata(self) -> dict[str, str]:
        return {"backend_version": "1.0", "data_version": "2025.1", "eos": "HEOS"}

    def get_property(self, property_name: str, state: StatePoint, fluid: FluidSpec) -> PropertyResult:
        return PropertyResult(
            name=property_name,
            quantity=Quantity(1.23, "SI"),
            metadata=BackendMetadata(backend=self.name),
        )

    def get_derivative(
        self,
        property_name: str,
        wrt: str,
        constant: str,
        state: StatePoint,
        fluid: FluidSpec,
    ) -> PropertyResult:
        return PropertyResult(
            name=f"d{property_name}/d{wrt}|{constant}",
            quantity=Quantity(0.1, "SI"),
            metadata=BackendMetadata(backend=self.name),
        )

    def flash(self, flash_spec: str, values: dict[str, Quantity], fluid: FluidSpec) -> FlashResult:
        return FlashResult(
            state={"T": Quantity(300.0, "K"), "p": Quantity(101325.0, "Pa")},
            phase="single_phase",
            metadata=BackendMetadata(backend=self.name),
        )


@dataclass(slots=True)
class NoFlashBackend(DummyBackend):
    name: str = "noflash"

    def capabilities(self) -> set[str]:
        return {"properties"}


def test_service_dispatch_and_metadata() -> None:
    service = PropsService()
    service.register_backend(DummyBackend(), make_default=True)

    state = StatePoint(inputs={"T": Quantity(300.0, "K"), "p": Quantity(1.0, "bar")})
    fluid = FluidSpec(name="Water")

    prop = service.get_property("cp", state, fluid)
    deriv = service.get_derivative("h", "T", "p", state, fluid)
    flash = service.flash("TP", state.inputs, fluid)
    meta = service.backend_metadata()

    assert prop.name == "cp"
    assert deriv.name == "dh/dT|p"
    assert flash.phase == "single_phase"
    assert meta.backend == "dummy"
    assert meta.options["eos"] == "HEOS"


def test_service_capability_and_backend_errors() -> None:
    service = PropsService()
    with pytest.raises(BackendNotAvailableError):
        service.capabilities()

    service.register_backend(NoFlashBackend(), make_default=True)
    state = StatePoint(inputs={"T": Quantity(300.0, "K"), "p": Quantity(1.0, "bar")})
    fluid = FluidSpec(name="Water")

    with pytest.raises(UnsupportedCapabilityError):
        service.flash("TP", state.inputs, fluid)
