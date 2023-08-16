from dash import dcc
import pandas as pd


def year_slider_2018(slider_id: str, years_min: int, years_max: int) -> dcc.RangeSlider:
    return dcc.RangeSlider(
        years_min, years_max, step=1, value=[2018, years_max],
        marks={i: str(i) for i in [years_min, 2018, years_max]},
        tooltip={"placement": "bottom", "always_visible": True},
        id=slider_id)



