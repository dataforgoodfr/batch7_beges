import uuid
import json
import time

import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State, ALL

from app import app
from utils.texts import TEXTS
from utils.organization_chart import OrganizationChart

from utils.organization_chart_html_wrapper import (
    EntityHtmlWrapper,
    OrganizationChartHtmlWrapper,
    oc_to_ochw,
    ochw_to_oc,
)

from utils.organization_chart import OrganizationChart

from apps.back_office_home import get_vertical_backoffice_navbar

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
        dbc.ModalBody(TEXTS["backoffice_organization_chart_help"]),
        dbc.ModalFooter(dbc.Button("Fermer", id="back-office-help-close-button", className="ml-auto")),
    ],
    id="back-office-help-modal",
)
entity_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.Row(dbc.Col(html.H4(id="back-office-entity-modal-header-title"), width=12)),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.Button(
                                "Supprimer l'entité",
                                id="back-office-entity-modal-delete-button",
                                color="danger",
                                style={"display": "none"},
                                block=True,
                            ),
                            dbc.Tooltip(
                                "Vous ne pouvez pas supprimer l'entité parce qu'elle possède d'autres entités ratachées à elle.",
                                id="back-office-entity-modal-delete-button-tooltip",
                                target="back-office-entity-modal-delete-button",
                                hide_arrow=True,
                                style={"display": "none"},
                                placement="right",
                            ),
                        ],
                        width=12,
                    )
                ),
            ],
            id="back-office-entity-modal-header",
        ),
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


layout = html.Div(
    dbc.Row(
        [
            dbc.Col(get_vertical_backoffice_navbar(), width=2),
            dbc.Col(
                [
                    html.Div(id="back-office-entity-tree", style={"display": "none"}),
                    html.Div(id="back-office-entity-selected", style={"display": "none"}),
                    html.H1("Gestion de l'organigramme", className="m-2"),
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            "Sauvegarder l'organigramme",
                                                            id="back-office-entities-save-organization-chart",
                                                            color="primary",
                                                            block=True,
                                                        ),
                                                        dbc.Tooltip(
                                                            "Sauvegarder l'organigramme et le publier.",
                                                            target="back-office-entities-save-organization-chart",
                                                            placement="bottom",
                                                        ),
                                                    ],
                                                    width=5,
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Ajouter une entité",
                                                        color="primary",
                                                        id="back-office-entity-new-modal-open-button",
                                                        block=True,
                                                    ),
                                                    width=5,
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Aide",
                                                        color="info",
                                                        id="back-office-help-toggle-button",
                                                        outline=True,
                                                        block=True,
                                                    ),
                                                    width=2,
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            dbc.Col(
                                                [
                                                    dbc.Alert(
                                                        "Une erreur s'est produite, l'organigramme n'a pas pu être sauvegardé !",
                                                        id="back-office-entities-save-organization-chart-error",
                                                        color="danger",
                                                        className="mt-3",
                                                        dismissable=True,
                                                        duration=10000,
                                                    ),
                                                    dbc.Alert(
                                                        "L'organigramme a bien été sauvegardé !",
                                                        id="back-office-entities-save-organization-chart-success",
                                                        color="success",
                                                        className="mt-3",
                                                        dismissable=True,
                                                        duration=10000,
                                                    ),
                                                ],
                                                width=12,
                                            )
                                        ),
                                    ]
                                )
                            ),
                            width=12,
                        )
                    ),
                    help_modal,
                    entity_modal,
                    html.Hr(),
                    dbc.Row([dbc.Col(html.Div(id="back-office-entity-tree-display"))]),
                ],
                width=10,
            ),
        ]
    )
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
    [
        Output("back-office-entity-modal", "is_open"),
        Output("back-office-entity-modal-mode", "children"),
        Output("back-office-entity-modal-entity-id", "children"),
        Output("back-office-entity-tree", "children"),
        Output("back-office-entity-tree-display", "children"),
    ],
    [
        Input({"type": "back-office-entity-expand", "id": ALL}, "n_clicks"),
        Input({"type": "back-office-entity-activated", "id": ALL}, "value"),
        # Modal update entity actions
        Input({"type": "back-office-entity-update-open-button", "id": ALL}, "n_clicks"),
        Input("back-office-entity-new-modal-open-button", "n_clicks"),
        Input("back-office-entity-modal-close-button", "n_clicks"),
        Input("back-office-entity-modal-valid-button", "n_clicks"),
        Input("back-office-entity-modal-delete-button", "n_clicks"),
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
    entity_modal_delete_button_n_clicks,
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
    # If the json tree is empty, we will load the tree from the app organization chart
    # Else we will load this json tree
    if not json_tree:

        oc = OrganizationChart()
        oc.load_current()
        ochw = oc_to_ochw(oc)
    else:
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
        elif element_full_id == "back-office-entity-modal-delete-button":
            entity = ochw.get_entity_by_id(state_modal_entity_id)
            entity.parent = None
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
                entity.expand = False
                ochw.toggle_entity_visible(entity.id)
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
                ochw.toggle_entity_visible(entity.id)
        else:
            element_full_id = json.loads(element_full_id)
            print(element_full_id)
            element_id = element_full_id["id"]
            element_type = element_full_id["type"]

            if element_type == "back-office-entity-activated":
                print(element_full_id)
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
        Output("back-office-entity-modal-header-title", "children"),
        Output("back-office-entity-modal-delete-button", "style"),
        Output("back-office-entity-modal-delete-button", "disabled"),
        Output("back-office-entity-modal-delete-button-tooltip", "style"),
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
            return (
                "Nouvelle entité",
                {"display": "none"},
                {"display": "none"},
                True,
                ochw.get_parent_options(),
                "",
                "",
                "",
                "",
            )
        elif modal_mode == "update":
            entity = ochw.get_entity_by_id(modal_entity_id)
            modal_header_title = "Modifier l'entité"
            modal_delete_button_style = {"display": "block"}
            # The condition to delete an entity is to have no children
            if entity.children:
                modal_delete_button_tooltip_style = {"display": "block"}
                modal_delete_button_disabled = True
            else:
                modal_delete_button_tooltip_style = {"display": "none"}
                modal_delete_button_disabled = False

            modal_parent_options = ochw.get_parent_options(entity.id)
            modal_label = entity.label
            modal_code_chorus = entity.code_chorus
            modal_code_odrive = entity.code_odrive
            modal_code_osfi = entity.code_osfi
            return (
                modal_header_title,
                modal_delete_button_style,
                modal_delete_button_disabled,
                modal_delete_button_tooltip_style,
                modal_parent_options,
                modal_label,
                modal_code_chorus,
                modal_code_odrive,
                modal_code_osfi,
            )
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


@app.callback(
    [
        Output("back-office-entities-save-organization-chart-error", "is_open"),
        Output("back-office-entities-save-organization-chart-success", "is_open"),
    ],
    [Input("back-office-entities-save-organization-chart", "n_clicks")],
    [State("back-office-entity-tree", "children")],
)
def save_organization_chart_and_publish(n_clicks, json_tree):
    if n_clicks:
        try:
            ochw = OrganizationChartHtmlWrapper()
            ochw.load_json(json_tree)
            local_oc = ochw_to_oc(ochw)
            filename = str(time.time_ns())
            local_oc.save_json(filename)
            local_oc.set_current(filename)
            return False, True
        except Exception as e:
            return True, False
    else:
        return False, False
