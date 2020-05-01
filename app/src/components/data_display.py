import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from components import chorus_dt

from app import app

layout = html.Div(
    id="div-data-display",
    children=[
        dbc.Tabs(
            id="tabs-datasets",
            children=[
                dbc.Tab(label="Déplacements train / avion", tab_id="chorus-dt"),
                dbc.Tab(label="Déplacements voiture", tab_id="odrive"),
                dbc.Tab(label="Consommation énergétiques", tab_id="osfi"),
            ],
            active_tab="chorus-dt",
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
    Output("tabs-content", "children"), [Input("selected-entity", "children"), Input("tabs-datasets", "active_tab")]
)
def on_selected_entity_fill_tabs_data(selected_entity, active_tab):
    if selected_entity is not None:
        organisation, service = selected_entity.split(";")
        if active_tab == "chorus-dt":
            return chorus_dt.layout
        elif active_tab == "odrive":
            return "ODRIVE, on going : (organisation : " + organisation + ", service : " + service + ")"
        elif active_tab == "osfi":
            return "OSFI, integration on going : (organisation : " + organisation + ", service : " + service + ")"
    else:
        return "empty"
