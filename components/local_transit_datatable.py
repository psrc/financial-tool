import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

from components import ids
from data.load_data_app import LocalTransitRevenue


def render(app: Dash, local_transit_revenue: LocalTransitRevenue) -> html.Div:

    @app.callback(
        Output(ids.LOCAL_TRANSIT_REVENUE_TABLE, "children"),
        Input(ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_DOLLAR_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_FORMAT_UNIT_DROPDOWN, "value")
    )
    def update_datatable(revenue_types: list[str], agencies: list[str], dollar: str = 'Nominal', value_unit: str = '') -> html.Div:

        filtered_data = local_transit_revenue.datatable(revenue_types=revenue_types, agencies=agencies, dollar=dollar, value_unit=value_unit)

        # return "No data selected." if nothing in table
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.")

        revenue_table = dash_table.DataTable(data=filtered_data.to_dict('records'),
                                             columns=[{"name": str(i), "id": str(i)} for i in filtered_data.columns],
                                             page_size=100)
        return html.Div(revenue_table, id=ids.LOCAL_TRANSIT_REVENUE_TABLE)

    return html.Div(id=ids.LOCAL_TRANSIT_REVENUE_TABLE)
