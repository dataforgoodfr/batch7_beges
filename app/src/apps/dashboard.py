from urllib.parse import parse_qs

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from apps import chorus_dt
from apps import odrive
from apps import osfi

from app import app

from utils.organization_chart import oc

layout = html.Div(
    id="div-data-display",
    children=[
        html.Div(id="dashboard-selected-entity", style={"display": "none"}),
        html.Div(id="dashboard-selected-entity-show"),
        dbc.Tabs(
            id="tabs-datasets",
            children=[
                dbc.Tab(label="Déplacements train / avion", tab_id="chorus-dt"),
                dbc.Tab(label="Déplacements voiture", tab_id="odrive"),
                dbc.Tab(label="Consommation énergétiques", tab_id="osfi"),
            ],
            active_tab="chorus-dt",
        ),
        html.Div(id="dashboard-selected-entity", style={"display": "none"}),
        html.Div(id="tabs-content"),
    ],
    style={"display": "none"},
)


@app.callback(Output("dashboard-selected-entity", "children"), [Input("url", "pathname")])
def parse_pathname(pathname):
    # Parsing the pathname which should be tableau_de_bord/{entity_id}
    entity_id = pathname.rsplit("/")[-1]
    return entity_id


@app.callback(Output("dashboard-selected-entity-show", "children"), [Input("dashboard-selected-entity", "children")])
def on_selected_entity_show_selected_entity(selected_entity):
    if selected_entity is not None:
        service = oc.get_entity_by_id(selected_entity)
        return html.Div(
            [
                html.H3(service.parent.label, style={"text-align": "center"}),
                html.Br(),
                html.H4(service.label, style={"text-align": "center"}),
            ]
        )


@app.callback(
    Output("div-data-display", "style"),
    [Input("dashboard-selected-entity", "children")],
    [State("div-data-display", "style")],
)
def on_selected_entity_toggle_tabs(selected_entity, style):
    if selected_entity is not None:
        style["display"] = "block"
        return style
    else:
        style["display"] = "none"
        return style


@app.callback(
    Output("tabs-content", "children"),
    [Input("dashboard-selected-entity", "children"), Input("tabs-datasets", "active_tab")],
)
def on_selected_entity_fill_tabs_data(selected_entity, active_tab):
    if selected_entity is not None:
        if active_tab == "chorus-dt":
            return chorus_dt.layout
        elif active_tab == "odrive":
            return odrive.layout
        elif active_tab == "osfi":
            return osfi.layout
    else:
        return "empty"
