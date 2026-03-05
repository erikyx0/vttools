import pandas as pd

from vttools import df_to_table


def test_df_to_table_latex_output() -> None:
    df = pd.DataFrame(
        {
            "name": ["run1", "run2"],
            "x": [1.2345, 10.0],
            "y": [12.3, 99.0],
        }
    )

    out = df_to_table(
        df,
        columns=["name", "x", "y"],
        rounding=["raw", ("f", 2), ("sig", 2)],
        latex=True,
    )

    assert "\\begin{tabular}" in out
    assert "run1 & 1.23 & 12 \\" in out


def test_df_to_table_plain_with_decimal_comma() -> None:
    df = pd.DataFrame({"x": [1.234]})

    out = df_to_table(
        df,
        columns=["x"],
        rounding=[3],
        latex=False,
        delimiter=";",
        decimal_sep=",",
    )

    assert out == "x\n1,234"


def test_df_to_table_latex_rules_order_and_duplicates() -> None:
    df = pd.DataFrame({"name": ["run1", "run2"], "x": [1.2, 2.3]})

    out = df_to_table(
        df,
        columns=["name", "x"],
        rounding=["raw", ("f", 1)],
        latex=True,
        latex_rules=[
            (0, "toprule"),
            (1, "midrule"),
            (2, "midrule"),
            (2, "midrule"),
            (3, "bottomrule"),
        ],
    )

    assert out == "\n".join(
        [
            r"\begin{tabular}{c | c}",
            r"\toprule",
            r"name & x \\",
            r"\midrule",
            r"run1 & 1.2 \\",
            r"\midrule",
            r"\midrule",
            r"run2 & 2.3 \\",
            r"\bottomrule",
            r"\end{tabular}",
        ]
    )


def test_df_to_table_latex_rules_validate_input() -> None:
    df = pd.DataFrame({"x": [1.0]})

    try:
        df_to_table(
            df,
            columns=["x"],
            rounding=[1],
            latex=True,
            latex_rules=[(99, "midrule")],
        )
        raise AssertionError("Expected ValueError for invalid position")
    except ValueError as exc:
        assert "Ungültige rule-Position" in str(exc)

    try:
        df_to_table(
            df,
            columns=["x"],
            rounding=[1],
            latex=True,
            latex_rules=[(1, "not-a-rule")],  # type: ignore[arg-type]
        )
        raise AssertionError("Expected ValueError for invalid rule name")
    except ValueError as exc:
        assert "Ungültiger Regelnamen" in str(exc)
