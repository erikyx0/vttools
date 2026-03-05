# Anforderungen an ein langfristig nutzbares Stoffdaten-Backend

Dieses Dokument ergänzt die aktuell geplanten Kernfunktionen (`property(T,p)`, kritische Daten, Diagramme) um Fähigkeiten, die in wissenschaftlichen und verfahrenstechnischen Anwendungen typischerweise unverzichtbar sind.

## 1. Modell- und Phasenrobustheit

- **Phasenbestimmung und Stabilitätsprüfung** (single-phase, Sattdampfgebiet, metastabil, Zweiphasengebiet).
- **Flash-Rechnungen** für übliche Kombinationen: `TP`, `PH`, `PS`, `UV`, `TQ`, `PQ`.
- **Sättigungseigenschaften**: Dampfdruckkurve, Siede-/Taupunkte, Verdampfungsenthalpie, Oberflächenspannung (wenn verfügbar).
- **Transporteigenschaften** konsistent in allen relevanten Bereichen: `mu`, `lambda`, `Pr`, Diffusivität.
- **Gültigkeitsbereiche und Warnungen** pro Korrelation/Backend (automatische Plausibilitäts-Flags).

## 2. Für Verfahrenstechnik essenzielle Eigenschaften

- **Ableitungen/Jacobians** für numerische Solver:
  - \\(\partial p / \partial T)_\rho\\, \\(\partial h / \partial T)_p\\, \\(\partial \rho / \partial p)_T\\ etc.
  - 2. Ableitungen für Sensitivität/Optimierung, wenn möglich.
- **Isentrope/isenthalpe Kennzahlen**: Schallgeschwindigkeit, Kompressibilität, Joule-Thomson-Koeffizient.
- **Referenzzustands-Management** (ASHRAE, IIR, NBP, benutzerdefiniert) mit transparenter Umrechnung.
- **Exergie-relevante Größen** (optional aber sehr nützlich): spezifische Exergie relativ zu definierter Umgebung.

## 3. Gemische und Stoffdatenverwaltung

- **Mehrkomponenten-Gemische** mit mole-/massenbezogener Zusammensetzung.
- **Mischungsregeln + Interaktionsparameter** (z. B. binäre Parameter, verschiedene EOS-Modelle).
- **VLE/LLE-Features**: K-Werte, Blasen-/Taupunktrechnung, Aktivitätskoeffizienten (modular).
- **Einheitliche Stoff-ID-Schicht**: Name, CAS, InChIKey, Synonyme, Alias-Mapping.
- **Metadatenzugriff**: Quellen, Versionsstand, Unsicherheiten, Zitierhinweis.

## 4. Architektur für Backend-Austausch (CoolProp, REFPROP, ...)

- **Klare Adapter-Schnittstelle** (Backend-agnostisch), z. B.:
  - `get_property(name, inputs, fluid, composition=None, backend="auto")`
  - `get_derivative(name, wrt, const, inputs, fluid, ...)`
  - `flash(spec, values, fluid, composition=None, ...)`
- **Capability Discovery**:
  - Laufzeitabfrage, welche Properties/Derivatives ein Backend wirklich kann.
  - Einheitliche Fallback-Strategien bei fehlenden Funktionen.
- **Reproduzierbarkeit durch Backend-Pinning**:
  - Backendname, Version, Datenbankstand, Optionen im Ergebnis mitschreiben.
- **Deterministische Fehlerklassen**:
  - `OutOfRangeError`, `BackendNotAvailableError`, `ConvergenceError`, `PhaseAmbiguityError`.

## 5. Numerik- und Workflow-Integration

- **Vektorisierte API** (NumPy-kompatibel) statt nur skalarer Calls.
- **Optionales JAX/Autograd-Interface** (oder finite-difference fallback), damit Gradienten in Optimierungen nutzbar sind.
- **Batch-Evaluierung + Caching** für große Parameterstudien.
- **Xarray/Pandas-Interoperabilität** für Design-of-Experiments, Sensitivitätsanalysen und Postprocessing.
- **Saubere Serialisierung** von Zuständen/Ergebnissen (JSON/Parquet), inkl. Einheiten und Backend-Metadaten.

## 6. Einheiten, Konsistenz, Qualitätssicherung

- **Striktes Einheitenkonzept** (SI intern, Ein-/Ausgabe mit Pint oder eigener Unit-Layer).
- **Konsistenztests**:
  - Maxwell-Relationen (wo anwendbar),
  - numerische Ableitungschecks,
  - Vergleich gegen Referenzdaten (NIST, REFPROP Benchmarks).
- **Regressionstest-Suite** je Backend und Fluid.
- **Unsicherheits-/Qualitätsflag** pro Ergebnis (z. B. extrapoliert, nahekritisch, geringe Datenlage).

## 7. Diagramme als Analysewerkzeug statt nur Plot-Funktion

- **Diagramm-Engine mit physikalischem Kontext**:
  - Sättigungslinien, Isobaren, Isothermen, Isentropen,
  - Zustandsweg-Overlays (Prozesspfade aus Simulationen).
- **Exportfähige Daten statt nur Figure** (für eigene Plot-Backends, Berichte, Dashboards).
- **Automatische Bereichswahl** je Fluid inkl. kritischer/sicherer Bereiche.

## 8. Empfohlene Minimal-Roadmap (praktisch umsetzbar)

1. **Core API + Einheitensystem + Fehlerklassen**.
2. **CoolProp-Adapter** mit scalar + vectorized Property Calls.
3. **Flash-Basisfunktionen (`TP`, `PH`, `PS`, `PQ`)** + Phasenflag.
4. **Derivative-API** für mindestens 5–10 Standardableitungen.
5. **Benchmark-/Regressionstests** gegen Referenzwerte.
6. **Backend-Abstraktion erweitern** (z. B. REFPROP-Adapter).
7. **Diagramm- und Workflow-Utilities** (xarray/pandas, Export, Caching).

## 9. Kurzfazit

Für eine „vollständige“ und langfristig nützliche Stoffdaten-Bibliothek reicht die reine Berechnung von Eigenschaften nicht aus. Der entscheidende Mehrwert entsteht durch:

- robuste Phasen- und Flash-Funktionalität,
- numerisch brauchbare Ableitungen,
- sauberes Einheiten- und Qualitätsmanagement,
- eine stabile, backend-agnostische Adapterarchitektur,
- und performante Integration in Simulation/Optimierung/Data-Science-Workflows.
