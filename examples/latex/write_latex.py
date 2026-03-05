import pandas as pd
from vttools import df_to_table
from vttools import write_tex

df = pd.DataFrame({"A":[1.234], "B":[5.678]})

table = df_to_table(
    df,
    columns=["A", "B"],
    rounding=[2, 2],
    latex=True,
    latex_rules="booktabs",
)

write_tex("report/tables/tab_results.tex", table)