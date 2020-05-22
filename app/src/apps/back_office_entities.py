import json

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State, MATCH, ALL

from anytree import LevelGroupOrderIter, PreOrderIter, RenderTree
from anytree.exporter import JsonExporter


from app import app

from utils.organization_chart_html_wrapper import EntityHtmlWrapper, OrganizationChartHtmlWrapper
from utils.organization_chart import OrganizationChart

# organization_chart = OrganizationChart("/data/entities_tree.tsv")
organization_chart = OrganizationChart("/data/entities_test_tree.tsv")


def load_oc_to_json(organization_chart):
    root = EntityHtmlWrapper(id="root", label="root")
    elements = {}
    elements["root"] = root
    for entity in PreOrderIter(organization_chart._root):
        print(entity)
        if entity.id == "root":
            continue
        parent_id = entity.parent.id
        entity = EntityHtmlWrapper(
            **{k: v for k, v in entity.__dict__.items() if (("parent" not in k) and ("children" not in k))},
            expand=False,
        )
        # Only displaying first level elements

        entity.parent = elements[parent_id]

        if entity.parent.id == "root":
            entity.visible = True

        elements[entity.id] = entity
    return JsonExporter().export(root)


oc_json = load_oc_to_json(organization_chart)


layout = html.Div(
    [
        html.Div(id="back-office-entity-tree", children=oc_json, style={"display": "none"}),
        html.Div(id="back-office-entity-selected", style={"display": "none"}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Charger un organigramme", id="load_organization_chart", color="primary", block=True),
                    width=4,
                ),
                dbc.Col(dbc.Button("Sauver l'organigramme", color="primary", block=True), width=4),
                dbc.Col(
                    dbc.Button("Aide", color="primary", id="help-toggle-button", outline=True, block=True), width=4
                ),
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Aide"),
                dbc.ModalBody("Voici un peu d'aide"),
                dbc.ModalFooter(dbc.Button("Fermer", id="help-close-button", className="ml-auto")),
            ],
            id="help-modal",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(html.Div(id="back-office-entity-tree-display"), width=8),
                dbc.Col(
                    html.Div(
                        id="back-office-organization-selected-items",
                        children=[
                            html.P(id="back-office-selected-entity"),
                            dbc.Form(
                                [
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Code Chorus dt"),
                                            dbc.Input(
                                                id="back-office-selected-entity-code-chorus",
                                                placeholder="Entrer code chorus dt",
                                            ),
                                            dbc.Label("Code Odrive"),
                                            dbc.Input(
                                                id="back-office-selected-entity-code-odrive",
                                                placeholder="Entrer code odrive",
                                            ),
                                            dbc.Label("Code Osfi"),
                                            dbc.Input(
                                                id="back-office-selected-entity-code-osfi",
                                                placeholder="Entrer code osfi",
                                            ),
                                        ]
                                    ),
                                    dbc.Button("Ok", color="primary"),
                                ]
                            ),
                        ],
                    ),
                    width=4,
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("help-modal", "is_open"),
    [Input("help-toggle-button", "n_clicks"), Input("help-close-button", "n_clicks")],
    [State("help-modal", "is_open")],
)
def toggle_help(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output("back-office-entity-tree", "children"), Output("back-office-entity-selected", "children")],
    [
        Input({"type": "back-office-entity", "id": ALL}, "n_clicks"),
        Input({"type": "back-office-entity-activated", "id": ALL}, "checked"),
        Input({"type": "back-office-entity-expand", "id": ALL}, "n_clicks"),
        # Input({"type": "back-office-entity-activity", "id": ALL}, "checked"),
    ],
    [State({"type": "back-office-entity", "id": ALL}, "id"), State("back-office-entity-tree", "children")],
)
def interact_organigram(select_n_clicks, activate_n_clicks, expand_n_clicks, all_ids, json_tree):
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)
    print(select_n_clicks, activate_n_clicks, expand_n_clicks, all_ids)

    # Loop over all interactions for each element
    selected_entity = None
    entity_to_set_activation = None
    entity_to_select = None
    entity_to_expand = None
    for div_id, select, activate, expand in zip(all_ids, select_n_clicks, activate_n_clicks, expand_n_clicks):
        if select:
            entity_to_select = div_id["id"]
        if expand:
            entity_to_expand = div_id["id"]
        if ochw.get_enitity_by_id(div_id["id"]).activated != activate:
            entity_to_set_activation = div_id["id"]
            entity_to_set_activation_activation = activate

    # Selecting if not activated
    if entity_to_select is not None:
        print("Select", entity_to_select)
        if entity_to_select != entity_to_set_activation and entity_to_select != entity_to_expand:
            ochw.toggle_select(entity_to_select)

    # Change activation
    if entity_to_set_activation is not None:
        ochw.toggle_activation(entity_to_set_activation)

    # expand entity
    if entity_to_expand is not None:
        ochw.toggle_expand(entity_to_expand)

    return ochw.to_json(), selected_entity


@app.callback(Output("back-office-entity-tree-display", "children"), [Input("back-office-entity-tree", "children")])
def display_elements(json_tree):
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)
    return ochw.get_html_elements()
