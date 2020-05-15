import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from app import app

layout = html.Div(
    id="div-header",
    children=[
        html.Div(id="div-url-redirect-to-entity-choice", style={"display": "none"}),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.P(
                            "Cet outil a été créé dans le crade de la saison 7 de data4good afin d'aider les différents services à créer leur Bilans d'émission de gaz à effet de serre (BEGES).",
                            style={"text-align": "center"},
                        ),
                        html.P(
                            "Cette application permet d'exploiter les principaux postes d'émissions de gaz à effet de serre detéctés :",
                            style={"text-align": "center"},
                        ),
                        html.Ul(
                            [
                                html.Li("Déplacements en train / avion,"),
                                html.Li("Déplacements en voiture,"),
                                html.Li("Dépenses énergétiques des batiments."),
                            ],
                            style={"width": "50%", "margin": "auto"},
                        ),
                    ]
                ),
                width={"size": 6, "offset": 3},
            )
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Selectionnez votre entité",
                    id="button-to-entity-choice",
                    color="primary",
                    className="mr-1",
                    block=True,
                ),
                width={"size": 2, "offset": 5},
            )
        ),
    ],
)


@app.callback(Output("div-url-redirect-to-entity-choice", "children"), [Input("button-to-entity-choice", "n_clicks")])
def on_click_go_to_entity_choice(n_clicks):
    if n_clicks:
        return dcc.Location(id="url-redirect-to-entity-choice", pathname="/selection_entite")
