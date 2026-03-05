"""Batch/parameter-study pattern for simulation and optimization loops.

Run:
    python examples/props/03_parameter_study.py
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from vttools.props import BackendMetadata, FluidSpec, PropertyResult, PropsService, Quantity, StatePoint


@dataclass(slots=True)
class StudyBackend:
    name: str = "study"

    def capabilities(self) -> set[str]:
        return {"properties"}

    def metadata(self) -> dict[str, str]:
        return {"backend_version": "0.3", "data_version": "study-v1", "source": "demo-correlation"}

    def get_property(self, property_name: str, state: StatePoint, fluid: FluidSpec) -> PropertyResult:
        temperature = state.inputs["T"].value
        pressure = state.inputs["p"].value

        if property_name == "mu":
            # simple monotonic demo-correlation
            mu = 1.0e-3 * (300.0 / temperature) ** 1.5 * (1.0 + 0.02 * (pressure / 1.0e5 - 1.0))
            return PropertyResult(
                name="mu",
                quantity=Quantity(mu, "Pa*s"),
                metadata=BackendMetadata(backend=self.name),
                quality_flags=("demo_correlation",),
            )

        raise ValueError(f"Unknown property: {property_name}")


def evaluate_viscosity_grid(service: PropsService, fluid: FluidSpec) -> list[dict[str, float]]:
    temperatures = [280.0, 300.0, 320.0, 340.0]
    pressures = [1.0e5, 2.0e5, 5.0e5]

    rows: list[dict[str, float]] = []
    for temperature in temperatures:
        for pressure in pressures:
            state = StatePoint(
                inputs={"T": Quantity(temperature, "K"), "p": Quantity(pressure, "Pa")},
                phase_hint="single_phase_liquid",
            )
            mu = service.get_property("mu", state, fluid)
            rows.append({"T_K": temperature, "p_Pa": pressure, "mu_Pa_s": mu.quantity.value})

    return rows


def choose_operating_point(rows: list[dict[str, float]]) -> dict[str, float]:
    """Example objective: minimize viscosity as proxy for pumping effort."""

    return min(rows, key=lambda row: row["mu_Pa_s"])


def main() -> None:
    service = PropsService()
    service.register_backend(StudyBackend(), make_default=True)

    fluid = FluidSpec(name="Water")
    rows = evaluate_viscosity_grid(service, fluid)

    print("=== Parameter Study (mu(T,p)) ===")
    for row in rows:
        print(f"T={row['T_K']:>6.1f} K | p={row['p_Pa']:>8.0f} Pa | mu={row['mu_Pa_s']:.6e} Pa*s")

    best = choose_operating_point(rows)
    avg_mu = mean(r["mu_Pa_s"] for r in rows)

    print("\n=== Simple analysis results ===")
    print(f"mean(mu): {avg_mu:.6e} Pa*s")
    print(
        "best point (min mu): "
        f"T={best['T_K']:.1f} K, p={best['p_Pa']:.0f} Pa, mu={best['mu_Pa_s']:.6e} Pa*s",
    )


if __name__ == "__main__":
    main()
