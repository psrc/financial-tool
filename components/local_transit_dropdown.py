import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from components import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_revenue_type = data['Revenue Type'].unique()
    all_agencies = data['Transit Agency'].unique()
    all_dollar_types = ["Nominal", "Constant"]
    all_format_units = ['', 'K', 'M']

    @app.callback(
        Output(ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_SELECT_ALL_REVENUE_TYPE, "n_clicks")
    )
    def select_all_revenue_types(_: int) -> list[str]:
        return all_revenue_type

    @app.callback(
        Output(ids.LOCAL_TRANSIT_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_SELECT_ALL_AGENCIES, "n_clicks")
    )
    def select_all_agencies(_: int) -> list[str]:
        return all_agencies

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
            html.H6("Format Unit"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_FORMAT_UNIT_DROPDOWN,
                options=[{"label": value_unit, "value": value_unit} for value_unit in all_format_units],
                value=""
            )
        ]
    )
