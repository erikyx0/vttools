from __future__ import annotations

from collections import defaultdict
from typing import Literal

import pandas as pd

from pathlib import Path

FormatSpec = int | str | tuple[str, int] | Literal["raw"]
RuleName = Literal["toprule", "midrule", "bottomrule"]
LatexRules = Literal["booktabs"] | list[tuple[int, RuleName]] | None


def df_to_table(
    df: pd.DataFrame,
    columns: list[str],
    rounding: list[FormatSpec],
    *,
    delimiter: str = " & ",
    decimal_sep: str = ".",
    latex: bool = True,
    latex_rules: LatexRules = None,
) -> str:
    """
    Erstellt LaTeX- oder CSV-ähnliche Tabellen aus einem DataFrame.

    Parameters
    ----------
    df:
        Eingabedaten als ``pandas.DataFrame``.
    columns:
        Auszugebende Spalten (in gewünschter Reihenfolge).
    rounding:
        Formatvorgabe pro Spalte. Erlaubte Einträge:
        - ``int``: Festpunkt mit n Nachkommastellen
        - ``str``: Direktes Python-Format, z. B. ``.2e``
        - ``("e", k)``: wissenschaftliche Notation
        - ``("f", k)``: Festpunkt
        - ``("sig", n)``: n signifikante Stellen
        - ``"raw"``: unverändert in Textform
    delimiter:
        Trennzeichen zwischen den Zellen.
    decimal_sep:
        Dezimaltrennzeichen, ``"."`` oder ``,``.
    latex:
        Falls ``True``, wird eine vollständige ``tabular``-Umgebung erzeugt.
    latex_rules:
        Optionales Regel-Array zur präzisen Platzierung von ``\\toprule``,
        ``\\midrule`` und ``\\bottomrule``. Jeder Eintrag ist ein Tupel
        ``(position, regelname)``.

        Positionsschema:
        - ``0``: direkt nach ``\\begin{tabular}``, vor der Kopfzeile
        - ``1``: direkt nach der Kopfzeile
        - ``2``: nach der ersten Datenzeile
        - ...
        - ``n + 1``: nach der ``n``-ten Datenzeile

        Mehrfachvorkommen sind erlaubt. Wenn ``None``, wird das bisherige
        Standardverhalten mit ``\\hline`` verwendet.

    Returns
    -------
    str
        Zusammengebaute Tabelle als String.
    """
    if len(columns) != len(rounding):
        raise ValueError("columns und rounding müssen gleich lang sein.")

    header = delimiter.join(columns)
    lines: list[str] = []
    table_rows: list[str] = []

    def fmt(value: object, spec: FormatSpec) -> str:
        if pd.isnull(value):
            return ""
        if spec == "raw":
            return str(value)

        if isinstance(spec, int):
            text = f"{value:.{spec}f}"
        elif isinstance(spec, str):
            text = f"{value:{spec}}"
        elif isinstance(spec, tuple):
            kind, num = spec
            if kind == "e":
                text = f"{value:.{num}e}"
            elif kind == "f":
                text = f"{value:.{num}f}"
            elif kind == "sig":
                text = f"{value:.{num}g}"
            else:
                raise ValueError(f"Unbekanntes Format-Tuple: {spec}")
        else:
            raise TypeError("rounding-Eintrag muss int, str, tuple oder 'raw' sein")

        if decimal_sep == ",":
            return text.replace(".", ",")
        return text

    for _, row in df.iterrows():
        cells = [fmt(row[col], spec) for col, spec in zip(columns, rounding)]
        table_rows.append(delimiter.join(cells))
    if latex and latex_rules == "booktabs":
        n = len(table_rows)
        latex_rules = [
            (0, "toprule"),
            (1, "midrule"),
            (n + 1, "bottomrule"),
        ]

    if latex:
        colspec = " | ".join("c" for _ in columns)
        lines = [rf"\begin{{tabular}}{{{colspec}}}"]

        if latex_rules is None:
            lines.extend([r"\hline", f"{header} \\\\ ", r"\hline"])
            lines.extend([f"{row} \\" for row in table_rows])
            lines.extend([r"\hline", r"\end{tabular}"])
            return "\n".join(lines)

        valid_rules: dict[str, str] = {
            "toprule": r"\toprule",
            "midrule": r"\midrule",
            "bottomrule": r"\bottomrule",
        }
        max_pos = len(table_rows) + 1
        rules_by_pos: dict[int, list[str]] = defaultdict(list)
        for pos, rule in latex_rules:
            if pos < 0 or pos > max_pos:
                raise ValueError(
                    f"Ungültige rule-Position {pos}. Erlaubt sind Werte von 0 bis {max_pos}."
                )
            if rule not in valid_rules:
                raise ValueError(
                    "Ungültiger Regelnamen. Erlaubt: 'toprule', 'midrule', 'bottomrule'."
                )
            rules_by_pos[pos].append(valid_rules[rule])

        lines.extend(rules_by_pos.get(0, []))
        lines.append(f"{header} \\")
        lines.extend(rules_by_pos.get(1, []))

        for idx, row in enumerate(table_rows, start=1):
            lines.append(f"{row} \\")
            lines.extend(rules_by_pos.get(idx + 1, []))

        lines.append(r"\end{tabular}")
    else:
        lines = [header, *table_rows]

    return "\n".join(lines)

def write_tex(path: str | Path, content: str, *, encoding: str = "utf-8") -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding, newline="\n")
    return path
