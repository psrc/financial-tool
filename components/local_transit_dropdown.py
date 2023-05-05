import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from components import ids
from data.load_data_app import DataSchema


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_revenue_type = data[DataSchema.REVENUE_TYPE].unique()
    all_agencies = data[DataSchema.TRANSIT_AGENCY].unique()
    all_dollar_types = ["Nominal", "Constant"]

    @app.callback(
        Output(ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_SELECT_ALL_REVENUE_TYPE, "n_clicks")
    )
    def select_all_revenue_type(_: int) -> list[str]:
        return all_revenue_type

    return html.Div(
        children=[
            html.H6("Revenue Type"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN,
                options=[{"label": revenue_type, "value": revenue_type} for revenue_type in all_revenue_type],
                value=all_revenue_type,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All Revenue Types"],
                id=ids.LOCAL_TRANSIT_SELECT_ALL_REVENUE_TYPE
            ),
            html.H6("Transit Agency"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_AGENCY_DROPDOWN,
                options=[{"label": agency, "value": agency} for agency in all_agencies],
                value=all_agencies,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All Transit Agencies"],
                id=ids.LOCAL_TRANSIT_SELECT_ALL_AGENCIES
            ),
            html.H6("Dollar Type"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_DOLLAR_TYPE_DROPDOWN,
                options=[{"label": dollar, "value": dollar} for dollar in all_dollar_types],
                value="Nominal"
            ),
            html.Button(
                className="dropdown-button",
                children=["Select Nominal Dollar or 2018 Constant Dollar"],
                id=ids.LOCAL_TRANSIT_SELECT_DOLLAR_TYPE
            )
        ]
    )
