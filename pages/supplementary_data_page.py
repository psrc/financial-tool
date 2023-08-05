import os
import toml
import dash
from dash import dcc, html
from components.supplementary_data_components import supplementary_data, supplementary_data_main

dash.register_page(__name__)

# read local transit data
data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))
supplementary_data_population = supplementary_data.PopulationData(data_config['result_subarea_population'])

tab_population = html.Div(children=[
    html.H1("Population data"),
    html.Hr(),
    # dropdown menu selecting revenue types + select all button
    supplementary_data_main.render_population_filter(supplementary_data_population.data),
    # local transit data table
    supplementary_data_main.render_population_datatable(supplementary_data_population)
]
)

layout = html.Div([
    html.H1("Supplementary Data"),
    dcc.Tabs(
        id="data-tabs",
        value='tab_data_population',
        parent_className='custom-tabs', className='custom-tabs-container',  # appends a class to the Tab component
        children=[
            dcc.Tab(label='Population Data',
                    value="tab_data_population",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    # appends a class to the Tab component when it is selected
                    children=[
                        tab_population
                    ]),
            dcc.Tab(label='Employment Data',
                    value="tab_data_employment",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                      dcc.Markdown('# Employment data\n'
                                   'Show employment data')
                    ])
        ]
    )
])
