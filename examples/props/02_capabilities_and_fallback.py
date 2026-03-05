"""Capability discovery and backend fallback strategies.

Run:
    python examples/props/02_capabilities_and_fallback.py
"""

from __future__ import annotations

from dataclasses import dataclass

from vttools.props import (
    BackendMetadata,
    FluidSpec,
    PropertyResult,
    PropsService,
    Quantity,
    StatePoint,
    UnsupportedCapabilityError,
)


@dataclass(slots=True)
class FastCpBackend:
    name: str = "fast_cp"

    def capabilities(self) -> set[str]:
        return {"properties"}

    def metadata(self) -> dict[str, str]:
        return {"backend_version": "1.0", "data_version": "fast-corr-v2"}

    def get_property(self, property_name: str, state: StatePoint, fluid: FluidSpec) -> PropertyResult:
        if property_name != "cp":
            raise ValueError("FastCpBackend supports only cp in this demo")
        return PropertyResult(
            name="cp",
            quantity=Quantity(4180.0, "J/(kg*K)"),
            metadata=BackendMetadata(backend=self.name),
        )


@dataclass(slots=True)
class FullBackend(FastCpBackend):
    name: str = "full"

    def capabilities(self) -> set[str]:
        return {"properties", "derivatives"}

    def get_derivative(
        self,
        property_name: str,
        wrt: str,
        constant: str,
        state: StatePoint,
        fluid: FluidSpec,
    ) -> PropertyResult:
        if (property_name, wrt, constant) != ("h", "T", "p"):
            raise ValueError("Only (dh/dT)_p is implemented in this demo")

        return PropertyResult(
            name="(dh/dT)_p",
            quantity=Quantity(4180.0, "J/(kg*K)"),
            metadata=BackendMetadata(backend=self.name),
        )


def main() -> None:
    service = PropsService()
    service.register_backend(FastCpBackend(), make_default=True)
    service.register_backend(FullBackend())

    state = StatePoint(inputs={"T": Quantity(300.0, "K"), "p": Quantity(1.0e5, "Pa")})
    fluid = FluidSpec(name="Water")

    print("=== Backends ===")
    for backend_name in service.list_backends():
        print(f"- {backend_name}: {sorted(service.capabilities(backend_name))}")

    cp_fast = service.get_property("cp", state, fluid, backend="fast_cp")
    print(f"cp via fast_cp: {cp_fast.quantity.value:.2f} {cp_fast.quantity.unit}")

    print("\nTry derivative on fast_cp (expected capability error)")
    try:
        _ = service.get_derivative("h", "T", "p", state, fluid, backend="fast_cp")
    except UnsupportedCapabilityError as exc:
        print(f"caught: {exc}")

    dhdt = service.get_derivative("h", "T", "p", state, fluid, backend="full")
    print(f"fallback to full backend -> {dhdt.name} = {dhdt.quantity.value:.2f} {dhdt.quantity.unit}")


if __name__ == "__main__":
    main()
