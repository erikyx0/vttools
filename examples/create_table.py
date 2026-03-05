"""Beispiel: Nutzung von vttools.df_to_table in einem Auswertungsskript."""

import pandas as pd

from vttools import df_to_table


def main1() -> None:
    df = pd.DataFrame(
        {
            "Run": ["A", "B", "C"],
            "U [m/s]": [2.0349, 2.4781, 1.9982],
            "Re": [1.2345e5, 1.5412e5, 1.2089e5],
            "eta": [0.82345, 0.84512, 0.80123],
        }
    )

    table = df_to_table(
        df,
        columns=["Run", "U [m/s]", "Re", "eta"],
        rounding=["raw", ("f", 2), ("e", 2), ("sig", 3)],
        decimal_sep=",",
        latex=True,
    )

    print(table)


def main2() -> None:
    df = pd.DataFrame(
        {
            "Run": ["A", "B", "C"],
            "U [m/s]": [2.0349, 2.4781, 1.9982],
            "Re": [1.2345e5, 1.5412e5, 1.2089e5],
            "eta": [0.82345, 0.84512, 0.80123],
        }
    )

    table = df_to_table(
        df,
        columns=["Run", "U [m/s]", "Re", "eta"],
        rounding=["raw", ("f", 2), ("e", 2), ("sig", 3)],
        decimal_sep=",",
        latex=True,
        latex_rules=[
            (0, "toprule"),
            (1, "midrule"),
            (len(df) + 1, "bottomrule"),
        ],
    )

    print(table)

def main3() -> None:
    df = pd.DataFrame(
        {
            "Run": ["A", "B", "C"],
            "U [m/s]": [2.0349, 2.4781, 1.9982],
            "Re": [1.2345e5, 1.5412e5, 1.2089e5],
            "eta": [0.82345, 0.84512, 0.80123],
        }
    )
    table = df_to_table(
        df,
        columns=["Run", "U [m/s]", "Re", "eta"],
        rounding=["raw", ("f", 2), ("e", 2), ("sig", 3)],
        decimal_sep=",",
        latex=True,
        latex_rules="booktabs"
    )
    print(table)

if __name__ == "__main__":
    main1()
    main2()
    main3()
