# main.py


from dash import Dash, html, dash_table
from dash_bootstrap_components.themes import BOOTSTRAP

# from components.layout import create_layout
from components.layout import create_layout_tabs


def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "2018 RTP Law Revenue"
    app.layout = create_layout_tabs(app)
    app.run_server(debug=True, port=1002)


if __name__ == "__main__":
    main()
