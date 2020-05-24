import json

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State, MATCH, ALL

from anytree import LevelGroupOrderIter, PreOrderIter, RenderTree
from anytree.exporter import JsonExporter


from app import app

from utils.organization_chart_html_wrapper import EntityHtmlWrapper, OrganizationChartHtmlWrapper, load_oc_to_json
from utils.organization_chart import OrganizationChart

organization_chart = OrganizationChart("/data/entities_tree.tsv")
# organization_chart = OrganizationChart("/data/entities_test_tree.tsv")


oc_json = load_oc_to_json(organization_chart)


def get_entity_modal(header, id_prefix):
    modal = dbc.Modal(
        [
            dbc.ModalHeader(header),
            dbc.ModalBody(
                html.Div(
                    children=[
                        html.P(id=id_prefix + "-selected-entity"),
                        dbc.Form(
                            [
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Code Chorus dt"),
                                        dbc.Input(id=id_prefix + "-code-chorus", placeholder="Entrer code chorus dt"),
                                        dbc.Label("Code Odrive"),
                                        dbc.Input(id=id_prefix + "-code-odrive", placeholder="Entrer code odrive"),
                                        dbc.Label("Code Osfi"),
                                        dbc.Input(id=id_prefix + "-code-osfi", placeholder="Entrer code osfi"),
                                    ]
                                ),
                                dbc.Button("Ok", color="primary"),
                            ]
                        ),
                    ]
                )
            ),
            dbc.ModalFooter(dbc.Button("Fermer", id=id_prefix + "-close-button", className="ml-auto")),
        ],
        id=id_prefix + "-modal",
    )
    return modal


new_node_modal = get_entity_modal("Nouvelle entité", "back-office-new-node")
update_node_modal = get_entity_modal("Mettre à jour entité", "back-office-update-node")


layout = html.Div(
    [
        html.Div(id="back-office-entity-tree", children=oc_json, style={"display": "none"}),
        html.Div(id="back-office-entity-selected", style={"display": "none"}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Charger un organigramme", id="load_organization_chart", color="primary", block=True),
                    width=5,
                ),
                dbc.Col(dbc.Button("Sauver l'organigramme", color="primary", block=True), width=5),
                dbc.Col(
                    dbc.Button("Aide", color="primary", id="back-office-help-toggle-button", outline=True, block=True),
                    width=2,
                ),
                dbc.Col(
                    dbc.Button(
                        "Ajouter entité",
                        color="primary",
                        id="back-office-new-node-toggle-button",
                        outline=True,
                        block=True,
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "Modifier entité",
                        color="primary",
                        id="back-office-update-node-toggle-button",
                        outline=True,
                        block=True,
                    ),
                    width=4,
                ),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Aide"),
                dbc.ModalBody("Voici un peu d'aide"),
                dbc.ModalFooter(dbc.Button("Fermer", id="back-office-help-close-button", className="ml-auto")),
            ],
            id="back-office-help-modal",
        ),
        new_node_modal,
        update_node_modal,
        html.Hr(),
        dbc.Row([dbc.Col(html.Div(id="back-office-entity-tree-display"))]),
    ]
)


@app.callback(
    Output("back-office-help-modal", "is_open"),
    [Input("back-office-help-toggle-button", "n_clicks"), Input("back-office-help-close-button", "n_clicks")],
    [State("back-office-help-modal", "is_open")],
)
def toggle_help(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("back-office-new-node-modal", "is_open"),
    [Input("back-office-new-node-toggle-button", "n_clicks"), Input("back-office-new-node-close-button", "n_clicks")],
    [State("back-office-new-node-modal", "is_open")],
)
def toggle_new_node(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("back-office-update-node-modal", "is_open"),
    [
        Input("back-office-update-node-toggle-button", "n_clicks"),
        Input("back-office-update-node-close-button", "n_clicks"),
    ],
    [State("back-office-update-node-modal", "is_open")],
)
def toggle_update_node(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("back-office-entity-tree", "children"),
    [
        Input({"type": "back-office-entity-activated", "id": ALL}, "checked"),
        Input({"type": "back-office-entity-expand", "id": ALL}, "n_clicks"),
    ],
    [State({"type": "back-office-entity", "id": ALL}, "id"), State("back-office-entity-tree", "children")],
)
def interact_organigram(activate_n_clicks, expand_n_clicks, all_ids, json_tree):
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)
    print(activate_n_clicks, expand_n_clicks, all_ids)

    # Loop over all interactions for each element
    entity_to_set_activation = None
    entity_to_expand = None
    for div_id, activate, expand in zip(all_ids, activate_n_clicks, expand_n_clicks):
        if expand:
            entity_to_expand = div_id["id"]
        if ochw.get_enitity_by_id(div_id["id"]).activated != activate:
            entity_to_set_activation = div_id["id"]
            entity_to_set_activation_activation = activate

    # Change activation
    if entity_to_set_activation is not None:
        ochw.toggle_activation(entity_to_set_activation)

    # expand entity
    if entity_to_expand is not None:
        ochw.toggle_expand(entity_to_expand)

    return ochw.to_json()


@app.callback(Output("back-office-entity-tree-display", "children"), [Input("back-office-entity-tree", "children")])
def display_elements(json_tree):
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)
    return ochw.get_html_elements()
