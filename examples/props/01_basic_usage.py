"""Basic usage of PropsService with a minimal backend adapter.

Run:
    python examples/props/01_basic_usage.py
"""

from __future__ import annotations

from dataclasses import dataclass

from vttools.props import BackendMetadata, FlashResult, FluidSpec, PropertyResult, PropsService, Quantity, StatePoint


@dataclass(slots=True)
class DemoBackend:
    """Tiny backend for demonstration.

    This class mimics an adapter around a real engine such as CoolProp/REFPROP.
    """

    name: str = "demo"

    def capabilities(self) -> set[str]:
        return {"properties", "derivatives", "flash"}

    def metadata(self) -> dict[str, str]:
        return {"backend_version": "0.1-demo", "data_version": "demo-db-2026", "model": "idealized"}

    def get_property(self, property_name: str, state: StatePoint, fluid: FluidSpec) -> PropertyResult:
        temperature = state.inputs["T"].value
        if property_name == "cp":
            cp_value = 4200.0 + 0.1 * (temperature - 300.0)
            return PropertyResult(
                name="cp",
                quantity=Quantity(cp_value, "J/(kg*K)"),
                metadata=BackendMetadata(backend=self.name),
            )
        if property_name == "rho":
            rho_value = 997.0 - 0.3 * (temperature - 293.15)
            return PropertyResult(
                name="rho",
                quantity=Quantity(rho_value, "kg/m^3"),
                metadata=BackendMetadata(backend=self.name),
            )

        raise ValueError(f"Unknown property: {property_name}")

    def get_derivative(
        self,
        property_name: str,
        wrt: str,
        constant: str,
        state: StatePoint,
        fluid: FluidSpec,
    ) -> PropertyResult:
        if (property_name, wrt, constant) == ("h", "T", "p"):
            return PropertyResult(
                name="(dh/dT)_p",
                quantity=Quantity(4200.0, "J/(kg*K)"),
                metadata=BackendMetadata(backend=self.name),
            )

        raise ValueError(f"Unsupported derivative: ({property_name}, {wrt}, {constant})")

    def flash(self, flash_spec: str, values: dict[str, Quantity], fluid: FluidSpec) -> FlashResult:
        if flash_spec != "TP":
            raise ValueError(f"Unsupported flash spec: {flash_spec}")

        return FlashResult(
            state={
                "T": values["T"],
                "p": values["p"],
                "h": Quantity(112_500.0, "J/kg"),
                "s": Quantity(392.0, "J/(kg*K)"),
            },
            phase="single_phase_liquid",
            metadata=BackendMetadata(backend=self.name),
        )


def main() -> None:
    service = PropsService()
    service.register_backend(DemoBackend(), make_default=True)

    state = StatePoint(inputs={"T": Quantity(298.15, "K"), "p": Quantity(101_325.0, "Pa")})
    fluid = FluidSpec(name="Water")

    cp = service.get_property("cp", state, fluid)
    rho = service.get_property("rho", state, fluid)
    dhdt = service.get_derivative("h", "T", "p", state, fluid)
    flash = service.flash("TP", state.inputs, fluid)
    metadata = service.backend_metadata()

    print("=== Basic PropsService Usage ===")
    print(f"Fluid: {fluid.name}")
    print(f"cp:  {cp.quantity.value:.2f} {cp.quantity.unit}")
    print(f"rho: {rho.quantity.value:.2f} {rho.quantity.unit}")
    print(f"(dh/dT)_p: {dhdt.quantity.value:.2f} {dhdt.quantity.unit}")
    print(f"flash phase: {flash.phase}")
    print(f"backend metadata: {metadata}")


if __name__ == "__main__":
    main()
