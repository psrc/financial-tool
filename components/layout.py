import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import os
import toml

from components import all_datatables, all_datatable_filters
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
            id="all-tabs", value='tab_local_transit_revenue',
            parent_className='custom-tabs', className='custom-tabs-container',
            children=[
                dcc.Tab(label='Local Transit Revenue', value="tab_local_transit_revenue",
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children=[tab_local_transit_revenue(app)]),
                dcc.Tab(label='Local Transit Boarding', value="tab-2",
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        children=[tab_local_transit_boarding(app)])
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
                              all_datatable_filters.render_local_transit_revenue(app, local_transit_revenue.data),
                              # local transit data table
                              all_datatables.render_local_transit_revenue(app, local_transit_revenue)
                              ]
                    )


def tab_local_transit_boarding(app: Dash) -> html.Div:
    """
    tab with local transit boarding table
    """
    local_transit_boarding = LocalTransitBoarding(data_config['result_boardings_local_transit'])

    return html.Div(children=[html.H1("Local Transit Boarding"),
                              html.Hr(),
                              # dropdown menu selecting revenue types + select all button
                              all_datatable_filters.render_local_transit_boarding(app, local_transit_boarding.data),
                              # local transit data table
                              all_datatables.render_local_transit_boarding(app, local_transit_boarding)
                              ]
                    )
