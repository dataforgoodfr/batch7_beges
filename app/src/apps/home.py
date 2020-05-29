import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from utils.texts import TEXTS

from app import app

layout = html.Div(
    id="div-header",
    children=[
        html.Div(id="home-div-url-redirect-to-about", style={"display": "none"}),
        html.Div(id="home-div-url-redirect-to-entity-choice", style={"display": "none"}),
        dbc.Row(dbc.Col(dcc.Markdown(TEXTS["home"]), width={"size": 6, "offset": 3})),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "En savoir plus",
                        id="button-to-about",
                        color="primary",
                        outline=True,
                        className="mr-1",
                        block=True,
                    ),
                    width={"size": 2, "offset": 4},
                ),
                dbc.Col(
                    dbc.Button(
                        "C'est parti !", id="button-to-entity-choice", color="primary", className="mr-1", block=True
                    ),
                    width={"size": 2, "offset": 0},
                ),
            ]
        ),
    ],
)


@app.callback(
    Output("home-div-url-redirect-to-entity-choice", "children"), [Input("button-to-entity-choice", "n_clicks")]
)
def on_click_go_to_entity_choice(n_clicks):
    if n_clicks:
        return dcc.Location(id="url-redirect-to-entity-choice", pathname="/selection_entite")


@app.callback(Output("home-div-url-redirect-to-about", "children"), [Input("button-to-about", "n_clicks")])
def on_click_go_to_about(n_clicks):
    if n_clicks:
        return dcc.Location(id="url-redirect-to-about", pathname="/a_propos")
