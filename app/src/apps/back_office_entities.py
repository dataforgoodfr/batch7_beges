import uuid
import json

import dash
from dash.exceptions import PreventUpdate
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

# organization_chart = OrganizationChart("/data/entities_tree.tsv")
organization_chart = OrganizationChart("/data/entities_test_tree.tsv")


oc_json = load_oc_to_json(organization_chart)
MODAL_ID_PREFIX = "back-office-entity-modal"


entity_modal_body = html.Div(
    children=[
        html.Div(id=MODAL_ID_PREFIX + "-entity-id", style={"display": "none"}),
        html.Div(id=MODAL_ID_PREFIX + "-mode", style={"display": "none"}),
        dbc.Form(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("Entité parente"),
                        dcc.Dropdown(id=MODAL_ID_PREFIX + "-parent", clearable=False),
                        dbc.Label("Libellé"),
                        dbc.Input(id=MODAL_ID_PREFIX + "-label", placeholder="Entrer libellé"),
                        dbc.Label("Code Chorus dt"),
                        dbc.Input(id=MODAL_ID_PREFIX + "-code-chorus", placeholder="Entrer code chorus dt"),
                        dbc.Label("Code Odrive"),
                        dbc.Input(id=MODAL_ID_PREFIX + "-code-odrive", placeholder="Entrer code odrive"),
                        dbc.Label("Code Osfi"),
                        dbc.Input(id=MODAL_ID_PREFIX + "-code-osfi", placeholder="Entrer code osfi"),
                    ]
                )
            ]
        ),
    ]
)


help_modal = dbc.Modal(
    [
        dbc.ModalHeader("Aide"),
        dbc.ModalBody("Voici un peu d'aide"),
        dbc.ModalFooter(dbc.Button("Fermer", id="back-office-help-close-button", className="ml-auto")),
    ],
    id="back-office-help-modal",
)
entity_modal = dbc.Modal(
    [
        dbc.ModalHeader("Nouvelle entité", id="back-office-entity-modal-header"),
        dbc.ModalBody(id="back-office-entity-modal-body", children=entity_modal_body),
        dbc.ModalFooter(
            [
                dbc.Button("Annuler", id="back-office-entity-modal-close-button", outline=True, color="primary"),
                dbc.Button("Valider", id="back-office-entity-modal-valid-button", color="primary"),
            ]
        ),
    ],
    id="back-office-entity-modal",
)
# update_entity_modal = dbc.Modal(
#     [
#         dbc.ModalHeader("Mettre à jour entité"),
#         dbc.ModalBody(
#             id="back-office-entity-update-modal-body", children=get_modal_body("back-office-entity-update-modal")
#         ),
#         dbc.ModalFooter(
#             [
#                 dbc.Button("Annuler", id="back-office-entity-update-modal-close-button", outline=True, color="primary"),
#                 dbc.Button("Valider", id="back-office-entity-update-modal-valid-button", color="primary"),
#             ],
#         ),
#     ],
#     id="back-office-entity-update-modal",
# )


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
                        id="back-office-entity-new-modal-open-button",
                        outline=True,
                        block=True,
                    ),
                    width=4,
                ),
            ]
        ),
        help_modal,
        entity_modal,
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


"""
@app.callback(
    [Output("back-office-pop-up-modal", "is_open"), Output("back-office-pop-up-modal", children)],
    [Input("back-office-pop-up-modal", "n_clicks"), Input("back-office-pop-up-modal", "n_clicks")],
    [State("back-office-pop-up-modal", "is_open"), State("back-office-entity-tree", "children")],
)
def toggle_new_node(n1, n2, is_open, json_tree):
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)
    if n1 or n2:
        return not is_open
    return is_open
"""


@app.callback(
    [
        Output("back-office-entity-modal", "is_open"),
        Output("back-office-entity-modal-mode", "children"),
        Output("back-office-entity-modal-entity-id", "children"),
        Output("back-office-entity-tree", "children"),
        Output("back-office-entity-tree-display", "children"),
    ],
    [
        Input({"type": "back-office-entity-expand", "id": ALL}, "n_clicks"),
        Input({"type": "back-office-entity-activated", "id": ALL}, "checked"),
        # Modal update entity actions
        Input({"type": "back-office-entity-update-open-button", "id": ALL}, "n_clicks"),
        Input("back-office-entity-new-modal-open-button", "n_clicks"),
        Input("back-office-entity-modal-close-button", "n_clicks"),
        Input("back-office-entity-modal-valid-button", "n_clicks"),
    ],
    [
        State("back-office-entity-tree", "children"),
        State("back-office-entity-modal-mode", "children"),
        State("back-office-entity-modal-entity-id", "children"),
        State("back-office-entity-modal-parent", "value"),
        State("back-office-entity-modal-label", "value"),
        State("back-office-entity-modal-code-chorus", "value"),
        State("back-office-entity-modal-code-odrive", "value"),
        State("back-office-entity-modal-code-osfi", "value"),
    ],
)
def interact_organigram(
    expand_n_clicks,
    activate_n_clicks,
    update_entity_modal_open_button_n_clicks,
    new_entity_modal_open_button_n_clicks,
    entity_modal_close_button_n_clicks,
    entity_modal_valid_button_n_clicks,
    json_tree,
    state_modal_mode,
    state_modal_entity_id,
    state_modal_parent_id,
    state_modal_label,
    state_modal_code_chorus,
    state_modal_code_odrive,
    state_modal_code_osfi,
):
    ctx = dash.callback_context
    ochw = OrganizationChartHtmlWrapper()
    ochw.load_json(json_tree)

    modal_is_open = None
    modal_mode = None
    modal_entity_id = None

    if not ctx.triggered:
        pass
    else:
        element_full_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if element_full_id == "back-office-entity-new-modal-open-button":
            modal_is_open = True
            modal_mode = "new"
        elif element_full_id == "back-office-entity-modal-close-button":
            modal_is_open = False
        elif element_full_id == "back-office-entity-modal-valid-button":
            modal_is_open = False
            if state_modal_mode == "new":
                entity = EntityHtmlWrapper(id=str(uuid.uuid4()), label=state_modal_label)
                entity.code_chorus = state_modal_code_chorus
                entity.code_odrive = state_modal_code_odrive
                entity.code_osfi = state_modal_code_osfi
                parent = ochw.get_entity_by_id(state_modal_parent_id)
                entity.parent = parent
                entity.visible = True
            elif state_modal_mode == "update":
                entity_id = state_modal_entity_id
                parent_id = state_modal_parent_id
                entity = ochw.get_entity_by_id(entity_id)
                parent = ochw.get_entity_by_id(parent_id)
                entity.parent = parent
                entity.label = state_modal_label
                entity.code_chorus = state_modal_code_chorus
                entity.code_odrive = state_modal_code_odrive
                entity.code_osfi = state_modal_code_osfi
        else:
            element_full_id = json.loads(element_full_id)
            element_id = element_full_id["id"]
            element_type = element_full_id["type"]

            if element_type == "back-office-entity-activated":
                ochw.toggle_activation(element_id)
            elif element_type == "back-office-entity-expand":
                ochw.toggle_expand(element_id)
            elif element_type == "back-office-entity-update-open-button":
                entity = ochw.get_entity_by_id(element_id)
                modal_is_open = True
                modal_mode = "update"
                modal_entity_id = entity.id

    return (modal_is_open, modal_mode, modal_entity_id, ochw.to_json(), ochw.get_html_elements())


@app.callback(
    [
        Output("back-office-entity-modal-parent", "options"),
        Output("back-office-entity-modal-label", "value"),
        Output("back-office-entity-modal-code-chorus", "value"),
        Output("back-office-entity-modal-code-odrive", "value"),
        Output("back-office-entity-modal-code-osfi", "value"),
    ],
    [Input("back-office-entity-modal", "is_open")],
    [
        State("back-office-entity-modal-mode", "children"),
        State("back-office-entity-modal-entity-id", "children"),
        State("back-office-entity-tree", "children"),
    ],
)
def fill_modal_body(modal_is_open, modal_mode, modal_entity_id, json_tree):
    """
    Fill the modal inputs / dropdown options depending on the mode and entity selected.
    """
    if modal_is_open:
        # Loading the tree
        ochw = OrganizationChartHtmlWrapper()
        ochw.load_json(json_tree)
        if modal_mode == "new":
            return ochw.get_parent_options(), "", "", "", ""
        elif modal_mode == "update":
            entity = ochw.get_entity_by_id(modal_entity_id)
            modal_parent_options = ochw.get_parent_options(entity.id)
            modal_label = entity.label
            modal_code_chorus = entity.code_chorus
            modal_code_odrive = entity.code_odrive
            modal_code_osfi = entity.code_osfi
            return modal_parent_options, modal_label, modal_code_chorus, modal_code_odrive, modal_code_osfi
    else:
        raise PreventUpdate


@app.callback(
    Output("back-office-entity-modal-parent", "value"),
    [Input("back-office-entity-modal-parent", "options")],
    [
        State("back-office-entity-modal", "is_open"),
        State("back-office-entity-modal-mode", "children"),
        State("back-office-entity-modal-entity-id", "children"),
        State("back-office-entity-tree", "children"),
    ],
)
def fill_modal_dropdown_value(options, is_open, modal_mode, modal_entity_id, json_tree):
    """
    If the modal is open, will choose the right value in the dropdown:
    - If the mode is new, it will choose "root"
    - If the mode is update, it will choose the entity parent
    """
    if not is_open:
        raise PreventUpdate
    else:
        if modal_mode == "new":
            return "root"
        else:
            ochw = OrganizationChartHtmlWrapper()
            ochw.load_json(json_tree)
            entity = ochw.get_entity_by_id(modal_entity_id)
            return entity.parent.id
