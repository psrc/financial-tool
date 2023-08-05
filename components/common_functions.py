from dash import dcc
import pandas as pd


def year_slider_2018(slider_id: str, years_min: int, years_max: int) -> dcc.RangeSlider:
    return dcc.RangeSlider(
        years_min, years_max, step=1, value=[2018, years_max],
        marks={i: str(i) for i in [years_min, 2018, years_max]},
        tooltip={"placement": "bottom", "always_visible": True},
        id=slider_id)


# change value format to thousands or millions
def format_value(df: pd.DataFrame, value_col: str, value_unit: str):

    df2 = df.copy()
    if value_unit in ['', 'K', 'M']:
        if value_unit == '':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x, 0)}")
        if value_unit == 'K':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000.0, 2)}{'K'}")
        if value_unit == 'M':
            df2[value_col] = df2[value_col].apply(lambda x: f"{round(x / 1000000.0, 2)}{'M'}")
    else:
        print("Value units must be 'K' for thousands or 'M' for millions")

    return df2
