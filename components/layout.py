import pandas as pd
from dash import Dash, html
import os
import toml

# from components.local_transit_dropdown import render
from components import local_transit_datatable, local_transit_dropdown
from data.load_data_app import LocalTransitRevenue

data_config = toml.load(os.path.join(os.getcwd(), "./configuration.toml"))


def create_layout(app: Dash) -> html.Div:
    local_transit_revenue = LocalTransitRevenue(data_config['tab_revenue_local_transit'])

    return html.Div(className="app-div",
                    children=[html.H1(app.title),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              html.Div(
                                  className="dropdown-container",
                                  children=[local_transit_dropdown.render(app, local_transit_revenue.data)]),
                              # local transit data table
                              local_transit_datatable.render(app, local_transit_revenue)
                              ]
                    )
