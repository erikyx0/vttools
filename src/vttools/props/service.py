"""Facade service that exposes a backend-agnostic props API."""

from __future__ import annotations

from dataclasses import dataclass, field

from .backend import PropsBackend
from .exceptions import BackendNotAvailableError, UnsupportedCapabilityError
from .models import BackendMetadata, FlashResult, FluidSpec, PropertyResult, Quantity, StatePoint


@dataclass(slots=True)
class PropsService:
    """Runtime backend registry and capability-aware dispatcher."""

    _backends: dict[str, PropsBackend] = field(default_factory=dict)
    default_backend: str | None = None

    def register_backend(self, backend: PropsBackend, *, make_default: bool = False) -> None:
        self._backends[backend.name] = backend
        if make_default or self.default_backend is None:
            self.default_backend = backend.name

    def list_backends(self) -> tuple[str, ...]:
        return tuple(sorted(self._backends))

    def capabilities(self, backend: str | None = None) -> set[str]:
        return self._resolve_backend(backend).capabilities()

    def get_property(
        self,
        property_name: str,
        state: StatePoint,
        fluid: FluidSpec,
        *,
        backend: str | None = None,
    ) -> PropertyResult:
        engine = self._resolve_backend(backend)
        return engine.get_property(property_name, state, fluid)

    def get_derivative(
        self,
        property_name: str,
        wrt: str,
        constant: str,
        state: StatePoint,
        fluid: FluidSpec,
        *,
        backend: str | None = None,
    ) -> PropertyResult:
        engine = self._resolve_backend(backend)
        if "derivatives" not in engine.capabilities():
            raise UnsupportedCapabilityError(
                f"Backend '{engine.name}' does not provide derivative calculations",
            )
        return engine.get_derivative(property_name, wrt, constant, state, fluid)

    def flash(
        self,
        flash_spec: str,
        values: dict[str, Quantity],
        fluid: FluidSpec,
        *,
        backend: str | None = None,
    ) -> FlashResult:
        engine = self._resolve_backend(backend)
        if "flash" not in engine.capabilities():
            raise UnsupportedCapabilityError(
                f"Backend '{engine.name}' does not provide flash calculations",
            )
        return engine.flash(flash_spec, values, fluid)

    def backend_metadata(self, backend: str | None = None) -> BackendMetadata:
        engine = self._resolve_backend(backend)
        metadata = engine.metadata()
        return BackendMetadata(
            backend=engine.name,
            backend_version=metadata.get("backend_version"),
            data_version=metadata.get("data_version"),
            options={k: v for k, v in metadata.items() if k not in {"backend_version", "data_version"}},
        )

    def _resolve_backend(self, backend: str | None) -> PropsBackend:
        name = backend or self.default_backend
        if not name:
            raise BackendNotAvailableError("No props backend registered")
        try:
            return self._backends[name]
        except KeyError as exc:
            raise BackendNotAvailableError(f"Backend '{name}' is not registered") from exc
