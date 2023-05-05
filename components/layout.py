import pandas as pd
from dash import Dash, html
from data import load_data_app

# from components.local_transit_dropdown import render
from components import local_transit_datatable, local_transit_dropdown


def create_layout(app: Dash) -> html.Div:
    data = load_data_app.load_local_transit_revenue_data('tab_revenue_local_transit')

    return html.Div(className="app-div",
                    children=[html.H1(app.title),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              html.Div(
                                  className="dropdown-container",
                                  children=[local_transit_dropdown.render(app, data)]),
                              # local transit data table
                              local_transit_datatable.render(app, data)
                              ]
                    )
