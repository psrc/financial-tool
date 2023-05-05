import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

from components import ids
import pandas as pd


def render(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(
        Output(ids.LOCAL_TRANSIT_REVENUE_TABLE, "children"),
        Input(ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_DOLLAR_TYPE_DROPDOWN, "value")
    )
    def update_datatable(revenue_types: list[str], agencies: list[str], dollar: str) -> html.Div:

        all_dollar_types = ["Nominal", "Constant"]
        remove_dollar = all_dollar_types.copy()
        remove_dollar.remove(dollar)
        col = data.columns.values.tolist()
        col.remove(remove_dollar[0])
        filtered_data = data[col].\
            query("`Revenue Type` in @revenue_types and `Transit Agency` in @agencies")

        # return "No data selected." if nothing in table
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.")

        revenue_table = dash_table.DataTable(data=filtered_data.to_dict('records'), page_size=100)
        return html.Div(revenue_table, id=ids.LOCAL_TRANSIT_REVENUE_TABLE)

    return html.Div(id=ids.LOCAL_TRANSIT_REVENUE_TABLE)
