from __future__ import annotations

from typing import Literal

import pandas as pd

FormatSpec = int | str | tuple[str, int] | Literal["raw"]


def df_to_table(
    df: pd.DataFrame,
    columns: list[str],
    rounding: list[FormatSpec],
    *,
    delimiter: str = " & ",
    decimal_sep: str = ".",
    latex: bool = True,
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

    Returns
    -------
    str
        Zusammengebaute Tabelle als String.
    """
    if len(columns) != len(rounding):
        raise ValueError("columns und rounding müssen gleich lang sein.")

    header = delimiter.join(columns)
    lines: list[str]
    if latex:
        header += r" \\ \hline"
        colspec = " | ".join("c" for _ in columns)
        lines = [rf"\begin{{tabular}}{{{colspec}}}", r"\hline", header]
        tail = [r"\hline", r"\end{tabular}"]
    else:
        lines, tail = [header], []

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
        line = delimiter.join(cells) + (r" \\" if latex else "")
        lines.append(line)

    lines.extend(tail)
    return "\n".join(lines)
