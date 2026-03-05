# vttools

Repository zur Sammlung nützlicher, wiederverwendbarer Tools für Aufgaben der Verfahrenstechnik.

## Zielbild für skalierbare Wiederverwendung

`vttools` ist als Python-Paket aufgebaut, damit Funktionen aus Einzelskripten zentral gepflegt und in vielen Projekten importiert werden können.

## Struktur

```text
vttools/
├── pyproject.toml         # Paket-Metadaten + Abhängigkeiten
├── src/
│   └── vttools/
│       ├── __init__.py    # öffentliche API
│       └── tables.py      # fachliche Utility-Module
├── tests/
│   └── test_tables.py     # automatisierte Tests
└── examples/
    └── create_table.py    # Mini-Skript als Nutzungsbeispiel
```

## Beispiel: Funktion aus Auswertungsskript integrieren

Die Funktion `df_to_table(...)` liegt jetzt in `src/vttools/tables.py` und wird über

```python
from vttools import df_to_table
```

importierbar gemacht. So bleiben Auswertungsskripte klein und die Formatierungslogik ist zentral versioniert/testbar.

## Entwicklung

### Installation (editable)

```bash
pip install -e .[dev]
```

### Tests

```bash
pytest
```

### Beispiel ausführen

```bash
python examples/create_table.py
```

## Empfohlene nächste Schritte

1. Weitere Themenmodule ergänzen (z. B. `units.py`, `plots.py`, `io.py`).
2. API bewusst klein halten: nur stabile Funktionen in `__init__.py` exportieren.
3. Für jede neue Utility direkt Tests + kleines Beispiel ergänzen.
4. Optional CI (GitHub Actions) aktivieren, um bei jedem Commit Tests laufen zu lassen.
