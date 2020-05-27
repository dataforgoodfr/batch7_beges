import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from apps import home
from apps import dashboard
from apps import entity_choice
from apps import about
from apps import methodology
from apps import footer

from app import app


navbar = dbc.Navbar(
    [dbc.NavbarBrand("Outil d'aide à la réalisation de Bilans d'Émissions de Gaz à Effet de Serre (BEGES)", href="/")],
    color="dark",
    dark=True,
    className="nav_bar",
)

app.layout = html.Div(
    children=[
        dbc.Container(
            [dcc.Location(id="url", refresh=False), navbar, html.Br(), html.Div(id="page-content")], fluid=True
        ),
        footer.layout,
    ]
)


flask_app = app.server

# Update the index
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/selection_entite":
        return entity_choice.layout
    elif isinstance(pathname, str) and pathname.startswith("/tableau_de_bord/"):
        return dashboard.layout
    elif pathname == "/a_propos":
        return about.layout
    elif pathname == "/methodologie":
        return methodology.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=80)
