import os
import toml
import dash
from dash import dcc, html
from components.local_transit_components import local_transit_data, local_transit_main

dash.register_page(__name__)

# read local transit data
data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))
local_transit_revenue = local_transit_data.LocalTransitRevenue(data_config['tab_revenue_local_transit'])
local_transit_boarding = local_transit_data.LocalTransitBoarding(data_config['result_boardings_local_transit'])


def tab_local_transit_revenue(revenue: local_transit_data.LocalTransitRevenue) -> html.Div:
    """
    tab with local transit revenue table
    """
    return html.Div(children=[html.H1("Local Transit Revenue"),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              local_transit_main.render_revenue_filter(revenue.data),
                              # local transit data table
                              local_transit_main.render_revenue_datatable(revenue)
                              ]
                    )


def tab_local_transit_boarding(boarding: local_transit_data.LocalTransitBoarding) -> html.Div:
    """
    tab with local transit boarding table
    """
    return html.Div(children=[html.H1("Local Transit Boarding"),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              local_transit_main.render_boarding_filter(boarding.data),
                              # local transit data table
                              local_transit_main.render_boarding_datatable(boarding)
                              ]
                    )


# local transit tap layout
layout = html.Div([
    html.H1("Local Transit"),
    dcc.Tabs(
        id="all-tabs",  # to identify dash components in callbacks
        value='tab_local_transit_revenue',  # determining which Tab is currently selected
        parent_className='custom-tabs', className='custom-tabs-container',  # appends a class to the Tab component
        children=[
            dcc.Tab(label='Local Transit Revenue', value="tab_local_transit_revenue",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    # appends a class to the Tab component when it is selected
                    children=[
                        tab_local_transit_revenue(local_transit_revenue)
                    ]),
            dcc.Tab(label='Local Transit Boarding', value="tab_local_transit_boarding",
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                        tab_local_transit_boarding(local_transit_boarding)
                    ])
        ]
    )
])


