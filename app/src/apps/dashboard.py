from flask import url_for
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from apps import chorus_dt
from apps import odrive
from apps import osfi
from app import app
from utils.organization_chart import OrganizationChart
from utils.texts import TEXTS

help_modal = dbc.Modal(
    [
        dbc.ModalHeader("Aide"),
        dbc.ModalBody(dcc.Markdown(TEXTS["dashboard_help"])),
        dbc.ModalFooter(dbc.Button("Fermer", id="dashboard-help-close-button", className="ml-auto")),
    ],
    id="dashboard-help-modal",
)

layout = html.Div(
    id="div-data-display",
    children=[
        html.Div(id="dashboard-div-url-redirect-to-entity-choice", style={"display": "none"}),
        html.Div(id="dashboard-selected-entity", style={"display": "none"}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        [html.I(className="fa fa-chevron-left fa-1x mr-1"), "Choisir une autre entité"],
                        id="dashboard-button-to-entity-choice",
                        href="/selection_entite",
                        color="primary",
                        outline=True,
                        block=True,
                    ),
                    width=3,
                ),
                dbc.Col(
                    html.A(
                        dbc.Button("Exporter toutes les données", color="primary", className="mr-1", block=True),
                        id="export-data-link",
                        href="",
                    ),
                    width={"size": 3, "offset": 4},
                ),
                dbc.Col(
                    dbc.Button(
                        "Aide", id="dashboard-help-toggle-button", color="secondary", className="mr-1", block=True
                    ),
                    width={"size": 2, "offset": 0},
                ),
            ],
            className="mb-3",
        ),
        help_modal,
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(id="dashboard-selected-entity-show", className="m-4"),
                                    width={"size": 10, "offset": 1},
                                )
                            ]
                        ),
                        dbc.Tabs(
                            id="tabs-datasets",
                            children=[
                                dbc.Tab(label="Déplacements train / avion", tab_id="chorus-dt"),
                                dbc.Tab(label="Déplacements voiture", tab_id="odrive"),
                                dbc.Tab(label="Consommation énergétiques", tab_id="osfi"),
                            ],
                            card=True,
                            className="nav-fill",
                            persistence=True,
                            active_tab="chorus-dt",
                        ),
                    ]
                ),
                dbc.CardBody(html.Div(id="tabs-content")),
            ]
        ),
    ],
    style={"display": "none"},
)


@app.callback([Output("export-data-link", "href")], [Input("dashboard-selected-entity", "children")])
def update_link(service):
    return [url_for("download_raw_excel", service=service)]


@app.callback(Output("dashboard-selected-entity", "children"), [Input("url", "pathname")])
def parse_pathname(pathname):
    # Parsing the pathname which should be tableau_de_bord/{entity_id}
    entity_id = pathname.rsplit("/")[-1]
    return entity_id


@app.callback(Output("dashboard-selected-entity-show", "children"), [Input("dashboard-selected-entity", "children")])
def on_selected_entity_show_selected_entity(selected_entity):
    if selected_entity is not None:
        oc = OrganizationChart()
        oc.load_current()
        service = oc.get_entity_by_id(selected_entity)
        return html.Div(
            [
                html.H3(service.parent.label, style={"text-align": "center"}),
                html.Br(),
                html.H4(service.label, style={"text-align": "center"}),
            ]
        )


@app.callback(
    Output("dashboard-help-modal", "is_open"),
    [Input("dashboard-help-toggle-button", "n_clicks"), Input("dashboard-help-close-button", "n_clicks")],
    [State("dashboard-help-modal", "is_open")],
)
def toggle_help(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
