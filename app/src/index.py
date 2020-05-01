import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from components import home
from components import datasets

from app import app


navbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(dbc.NavbarBrand("Outil d'aide à la création de BEGES", className="ml-2"))
            ]
        )
    ],
    className="nav_bar"
)

app.layout = dbc.Container(
    [
        html.Div(id="div-url-redirect"),
        dcc.Location(id="url", refresh=False),
        navbar,
        #html.H1("Outil d'aide à la création de BEGES", style={"text-align": "center", "margin-top": "5%"}),
        #html.Hr(),
        html.Br(),
        html.Div(id="page-content"),
    ],
    fluid=True
)
flask_app = app.server

# Update the index
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/datasets":
        return datasets.layout


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=80)
