import dash
from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP


app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=True)
app.layout = html.Div(
    [
        # main app framework
        html.Div("2018 RTP Law Revenue", style={'fontSize': 50, 'textAlign': 'center'}),
        html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'])
            for page in dash.page_registry.values()
        ]),
        html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
