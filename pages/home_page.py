import dash
from dash import dcc, html

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        dcc.Markdown('# Financial Tool Home Page\n'
                     'Current functions: local transit revenue and boarding')
    ]
)
