import pandas as pd
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output

from components import ids, common_functions
from components.supplementary_data_components import supplementary_data


def render_population_datatable(population: supplementary_data.PopulationData) -> html.Div:

    datatable = html.Div(className="transit-all-year-table", id="supplementary_data-population-table")

    @callback(
        Output("supplementary_data-population-table", "children"),
        Input("supplementary-population_county-dropdown", "value"),
        Input("supplementary-population-slider", "value"),
        Input("supplementary-population_format-unit-radio-item", "value")
    )
    def update_datatable(counties: list[str], slider_year: list[int], value_unit: str = '') -> html.Div:

        filtered_data = population.datatable(counties=counties, slider_year=slider_year, value_unit=value_unit)

        # return "No data selected." if nothing in table
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id="supplementary_data-population-table")
        else:
            population_table = dash_table.DataTable(
                data=filtered_data.to_dict('records'),
                columns=[{"name": str(i), "id": str(i)} for i in filtered_data.columns],
                page_size=100,
                include_headers_on_copy_paste=True
            )
            return html.Div(population_table, id="supplementary_data-population-table")

    return datatable


def render_population_filter(data: pd.DataFrame) -> html.Div:
    all_counties = data['County'].unique()
    years_min = data['Year'].min()
    years_max = data['Year'].max()
    all_format_units = ['', 'K', 'M']

    filter_box = html.Div(
        children=[
            html.H6("Counties"),
            dcc.Dropdown(
                id="supplementary-population_county-dropdown",
                options=[{"label": county, "value": county} for county in all_counties],
                value=all_counties,
                multi=True
            ),
            html.Button(
                id="supplementary-population_select-all-counties",
                className="dropdown-button",
                children=["Select All Counties"]
            ),
            html.H6("Format Unit"),
            dcc.RadioItems(
                id="supplementary-population_format-unit-radio-item",
                options=[{"label": value_unit, "value": value_unit} for value_unit in all_format_units],
                value=""
            ),
            html.H6("Year Range"),
            common_functions.year_slider_2018(slider_id="supplementary-population-slider",
                                              years_min=years_min, years_max=years_max)
        ]
    )

    @callback(
        Output("supplementary-population_county-dropdown", "value"),
        Input("supplementary-population_select-all-counties", "n_clicks")
    )
    def select_all_counties(_: int) -> list[str]:
        return all_counties

    return filter_box
