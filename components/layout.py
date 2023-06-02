import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import os
import toml

# from components.local_transit_dropdown import render
from components import local_transit_datatable, local_transit_dropdown
from data.load_data_app import LocalTransitRevenue, LocalTransitBoarding

data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))


# main layout with all tabs
def create_layout_tabs(app: Dash) -> html.Div:
    """
    main layout with all tabs
    """
    return html.Div([
        html.H1(app.title),
        dcc.Tabs(
            id="all-tabs", value='tab_local_transit_revenue', children=[
                dcc.Tab(label='Local Transit Revenue', value="tab_local_transit_revenue",
                        children=[tab_local_transit_revenue(app)]),
                dcc.Tab(label='Tab two', value="tab-2",
                        children=[html.H1("Tab 2")])
            ]
        )
    ])


def tab_local_transit_revenue(app: Dash) -> html.Div:
    """
    tab with local transit revenue table
    """
    local_transit_revenue = LocalTransitRevenue(data_config['tab_revenue_local_transit'])

    return html.Div(children=[html.H1("Local Transit Revenue"),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              local_transit_dropdown.render(app, local_transit_revenue.data),
                              # local transit data table
                              local_transit_datatable.render(app, local_transit_revenue)
                              ]
                    )


# def tab_local_transit_boarding(app: Dash) -> html.Div:
#     """
#     tab with local transit boarding table
#     """
#     local_transit_boarding = LocalTransitBoarding(data_config['result_boardings_local_transit'])
#
#     return html.Div(children=[html.H1(app.title + ": Local Transit Boarding"),
#                               html.Hr(),
#                               # dropdown menu selecting revenue types + select all button
#                               local_transit_dropdown.render_local_transit_boarding(app, local_transit_boarding.data),
#                               # local transit data table
#                               local_transit_datatable.render_local_transit_boarding(app, local_transit_boarding)
#                               ]
#                     )
