import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from utils.texts import TEXTS

from app import app

layout = html.Div(
    id="div-header",
    children=[
        dbc.Row(
            dbc.Col(
                [html.H1("Outil BEGES", className="my-5"), dcc.Markdown(TEXTS["home"])], width={"size": 6, "offset": 3}
            ),
            className="mb-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "En savoir plus",
                        id="button-to-about",
                        color="primary",
                        outline=True,
                        block=True,
                        href="/a_propos",
                    ),
                    width={"size": 2, "offset": 4},
                ),
                dbc.Col(
                    dbc.Button(
                        "C'est parti !",
                        id="button-to-entity-choice",
                        color="primary",
                        block=True,
                        href="/selection_entite",
                    ),
                    width={"size": 2, "offset": 0},
                ),
            ],
            className="mb-5",
        ),
    ],
)
