# Beispiele für `vttools.props`

Diese Beispiele zeigen typische Nutzungsmuster für das neue Stoffdaten-Backend-Interface.

## Inhalte

- `01_basic_usage.py`  
  Registrierung eines Backends, Property-/Derivative-/Flash-Call und Metadaten.
- `02_capabilities_and_fallback.py`  
  Capability-Discovery, gezielter Backend-Wechsel und Fehlerbehandlung.
- `03_parameter_study.py`  
  Vektor-/Batch-Workflow für Studien, der in Simulation und Optimierung wiederverwendbar ist.

## Ausführen

```bash
python examples/props/01_basic_usage.py
python examples/props/02_capabilities_and_fallback.py
python examples/props/03_parameter_study.py
```

> Hinweis: Die Beispiele nutzen bewusst Dummy-Backends (ohne CoolProp/REFPROP), damit sie sofort lokal laufen.
> Das gleiche Muster kann direkt auf echte Adapter übertragen werden.
