import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from components import chorus_dt
from components import odrive

from app import app

layout = html.Div(
    id="div-data-display",
    children=[
        dcc.Tabs(
            id="tabs-datasets",
            value="chorus-dt",
            children=[
                dcc.Tab(label="Déplacements train / avion", value="chorus-dt"),
                dcc.Tab(label="Déplacements voiture", value="odrive"),
                dcc.Tab(label="Consommation énergétiques", value="osfi"),
            ],
        ),
        html.Div(id="tabs-content"),
    ],
    style={"display": "none"},
)


@app.callback(
    Output("div-data-display", "style"), [Input("selected-entity", "children")], [State("div-data-display", "style")]
)
def on_selected_entity_toggle_tabs(selected_entity, style):
    if selected_entity is not None:
        style["display"] = "block"
        return style
    else:
        style["display"] = "none"
        return style


@app.callback(
    Output("tabs-content", "children"), [Input("selected-entity", "children"), Input("tabs-datasets", "value")]
)
def on_selected_entity_fill_tabs_data(selected_entity, active_tab):
    if selected_entity is not None:
        organisation, service = selected_entity.split(";")
        if active_tab == "chorus-dt":
            return chorus_dt.layout
        elif active_tab == "odrive":
            return odrive.layout
        elif active_tab == "osfi":
            return "OSFI, integration on going : (organisation : " + organisation + ", service : " + service + ")"
    else:
        return "empty"
