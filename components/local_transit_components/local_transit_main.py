import pandas as pd
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output

from components import ids, common_components
from components.local_transit_components import local_transit_data


#####################################################
# datatables
#####################################################
def render_revenue_datatable(local_transit_revenue: local_transit_data.LocalTransitRevenue) -> html.Div:

    datatable = html.Div(id=ids.LOCAL_TRANSIT_REVENUE_TABLE)

    @callback(
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
            revenue_table = dash_table.DataTable(
                data=filtered_data.to_dict('records'),
                columns=[{"name": str(i), "id": str(i)} for i in filtered_data.columns],
                page_size=100,
                include_headers_on_copy_paste=True,
                # change color for row of total agency revenue
                style_data_conditional=[
                     {
                         'if': {'filter_query': '{Revenue Type} = "Total"'},
                         'backgroundColor': '#91268F',
                         'color': 'white'
                     }
                ]
            )
            return html.Div(revenue_table, id=ids.LOCAL_TRANSIT_REVENUE_TABLE)

    return datatable


def render_boarding_datatable(local_transit_boarding: local_transit_data.LocalTransitBoarding) -> html.Div:

    datatable = html.Div(className="transit-all-year-table", id=ids.LOCAL_TRANSIT_BOARDING_TABLE)

    @callback(
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

    return datatable


#####################################################
# local transit filtering dropdowns and radio buttons
#####################################################
def render_revenue_filter(data: pd.DataFrame) -> html.Div:
    all_revenue_type = data['Revenue Type'].unique()
    all_agencies = data['Transit Agency'].unique()
    years_min = data['Year'].min()
    years_max = data['Year'].max()
    all_dollar_types = ["Nominal", "Constant"]
    all_format_units = ['', 'K', 'M']

    filter_box = html.Div(
        children=[
            html.H6("Revenue Type"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN,
                options=[{"label": revenue_type, "value": revenue_type} for revenue_type in all_revenue_type],
                value=all_revenue_type,
                placeholder="Select any revenue type",
                multi=True
            ),
            html.Button(
                id=ids.LOCAL_TRANSIT_SELECT_ALL_REVENUE_TYPE,
                children=["Select All Revenue Types"]
            ),
            html.H6("Transit Agency"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_AGENCY_DROPDOWN,
                options=[{"label": agency, "value": agency} for agency in all_agencies],
                value=all_agencies,
                placeholder="Select any transit agency",
                multi=True
            ),
            html.Button(
                id=ids.LOCAL_TRANSIT_SELECT_ALL_AGENCIES,
                children=["Select All Transit Agencies"]
            ),
            html.H6("Dollar Type"),
            dcc.RadioItems(
                id=ids.LOCAL_TRANSIT_DOLLAR_TYPE_DROPDOWN,
                options=[{"label": dollar, "value": dollar} for dollar in all_dollar_types],
                value="Nominal"
            ),
            html.H6("Format Unit"),
            dcc.RadioItems(
                id=ids.LOCAL_TRANSIT_FORMAT_UNIT_DROPDOWN,
                options=[{"label": value_unit, "value": value_unit} for value_unit in all_format_units],
                value=""
            ),
            html.H6("Year Range"),
            common_components.year_slider_2018(slider_id=ids.LOCAL_TRANSIT_REVENUE_YEAR_SLIDER,
                                               years_min=years_min, years_max=years_max)
        ]
    )

    @callback(
        Output(component_id=ids.LOCAL_TRANSIT_REVENUE_TYPE_DROPDOWN, component_property="value"),
        Input(component_id=ids.LOCAL_TRANSIT_SELECT_ALL_REVENUE_TYPE, component_property="n_clicks")
    )
    def select_all_revenue_types(_: int) -> list[str]:
        return all_revenue_type

    @callback(
        Output(ids.LOCAL_TRANSIT_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_SELECT_ALL_AGENCIES, "n_clicks")
    )
    def select_all_agencies(_: int) -> list[str]:
        return all_agencies

    return filter_box


def render_boarding_filter(data: pd.DataFrame) -> html.Div:
    all_agencies = data['Transit Agency'].unique()
    years_min = data['Year'].min()
    years_max = data['Year'].max()
    all_format_units = ['', 'K', 'M']

    filter_box = html.Div(
        children=[
            html.H6("Transit Agency"),
            dcc.Dropdown(
                id=ids.LOCAL_TRANSIT_BOARDING_AGENCY_DROPDOWN,
                options=[{"label": agency, "value": agency} for agency in all_agencies],
                value=all_agencies,
                multi=True
            ),
            html.Button(
                id=ids.LOCAL_TRANSIT_BOARDING_SELECT_ALL_AGENCIES,
                className="dropdown-button",
                children=["Select All Transit Agencies"]
            ),
            html.H6("Format Unit"),
            dcc.RadioItems(
                id=ids.LOCAL_TRANSIT_BOARDING_FORMAT_UNIT_DROPDOWN,
                options=[{"label": value_unit, "value": value_unit} for value_unit in all_format_units],
                value=""
            ),
            html.H6("Year Range"),
            common_components.year_slider_2018(slider_id=ids.LOCAL_TRANSIT_BOARDING_YEAR_SLIDER,
                                               years_min=years_min, years_max=years_max)
        ]
    )

    @callback(
        Output(ids.LOCAL_TRANSIT_BOARDING_AGENCY_DROPDOWN, "value"),
        Input(ids.LOCAL_TRANSIT_BOARDING_SELECT_ALL_AGENCIES, "n_clicks")
    )
    def select_all_agencies(_: int) -> list[str]:
        return all_agencies

    return filter_box
