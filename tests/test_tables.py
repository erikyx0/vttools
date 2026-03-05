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
