"""
# datatables connected to filtering components in `all_datatable_filters.py`
- local transit revenue
- local transit boarding
"""
# TODO: put boarding datatable underneath revenue datatable and use the same filtering dropdowns

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

from components import ids
from data.load_data_app import LocalTransitRevenue, LocalTransitBoarding


def render_local_transit_revenue(app: Dash, local_transit_revenue: LocalTransitRevenue) -> html.Div:
    @app.callback(
        Output(ids.LOCAL_TRANSIT_REVENUE_TABLE, "children"),
        Input(ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_REVENUE_YEAR_SLIDER, "value"),
        Input(ids.LOCAL_TRANSIT_DOLLAR_TYPE_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_FORMAT_UNIT_DROPDOWN, "value")
    )
    def update_datatable(revenue_types: list[str], agencies: list[str],
                         slider_year: list[int], dollar: str = 'Nominal', value_unit: str = '') -> html.Div:

        filtered_data = local_transit_revenue.datatable(revenue_types=revenue_types, agencies=agencies,
                                                        slider_year=slider_year, dollar=dollar,
                                                        value_unit=value_unit)

        # return "No data selected." if nothing in table
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.LOCAL_TRANSIT_REVENUE_TABLE)
        else:
            revenue_table = dash_table.DataTable(data=filtered_data.to_dict('records'),
                                                 columns=[{"name": str(i), "id": str(i)} for i in
                                                          filtered_data.columns],
                                                 page_size=100,
                                                 include_headers_on_copy_paste=True,
                                                 # change color for row of total agency revenue
                                                 style_data_conditional=[
                                                     {
                                                         'if': {
                                                             'filter_query': '{Revenue Type} = "Total"',
                                                         },
                                                         'backgroundColor': '#91268F',
                                                         'color': 'white'
                                                     },
                                                 ]
                                                 )
            return html.Div(revenue_table, id=ids.LOCAL_TRANSIT_REVENUE_TABLE)

    return html.Div(className="transit-all-year-table", id=ids.LOCAL_TRANSIT_REVENUE_TABLE)


def render_local_transit_boarding(app: Dash, local_transit_boarding: LocalTransitBoarding) -> html.Div:
    @app.callback(
        Output(ids.LOCAL_TRANSIT_BOARDING_TABLE, "children"),
        Input(ids.LOCAL_TRANSIT_BOARDING_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_BOARDING_YEAR_SLIDER, "value"),
        Input(ids.LOCAL_TRANSIT_BOARDING_FORMAT_UNIT_DROPDOWN, "value")
    )
    def update_datatable(agencies: list[str], slider_year: list[int], value_unit: str = '') -> html.Div:

        filtered_data = local_transit_boarding.datatable(agencies=agencies, slider_year=slider_year, value_unit=value_unit)

        # return "No data selected." if nothing in table
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.LOCAL_TRANSIT_BOARDING_TABLE)
        else:
            boarding_table = dash_table.DataTable(data=filtered_data.to_dict('records'),
                                                  columns=[{"name": str(i), "id": str(i)} for i in filtered_data.columns],
                                                  page_size=100,
                                                  include_headers_on_copy_paste=True
                                                  )
            return html.Div(boarding_table, id=ids.LOCAL_TRANSIT_BOARDING_TABLE)

    return html.Div(className="transit-all-year-table", id=ids.LOCAL_TRANSIT_BOARDING_TABLE)
