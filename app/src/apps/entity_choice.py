import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input, State

from utils.organization_chart import oc
from app import app


layout = html.Div(
    id="div-entity-choice",
    children=[
        html.Div(id="entity-choice-div-url-redirect-to-dashboard", style={"display": "none"}),
        html.Div(id="entity-choice-selected-entity", style={"display": "none"}),
        dcc.Dropdown(
            id="dropdown-entity-choice-level-1",
            options=oc.get_level_1_dropdown_items(),
            placeholder="Choisissez votre organisation",
            clearable=True,
            style={"margin": "10px"},
        ),
        dcc.Dropdown(
            id="dropdown-entity-choice-level-2",
            placeholder="Choisissez votre service",
            clearable=True,
            style={"margin": "10px", "display": "none"},
        ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Afficher les données",
                    id="button-to-dashboard",
                    color="primary",
                    className="mr-1",
                    style={"display": "none"},
                ),
                width={"size": 2, "offset": 5},
            )
        ),
    ],
)


@app.callback(
    Output("entity-choice-div-url-redirect-to-dashboard", "children"),
    [Input("button-to-dashboard", "n_clicks")],
    [State("entity-choice-selected-entity", "children")],
)
def on_click_go_to_dashboard(n_clicks, selected_entity):
    if n_clicks:
        organization, service = oc.get_organization_service(selected_entity)
        return dcc.Location(id="url-redirect-to-dashboard", pathname="/tableau_de_bord/%s" % service.id)


@app.callback(
    [
        Output("dropdown-entity-choice-level-2", "style"),
        Output("dropdown-entity-choice-level-2", "options"),
        Output("dropdown-entity-choice-level-2", "value"),
    ],
    [Input("dropdown-entity-choice-level-1", "value")],
    [State("dropdown-entity-choice-level-2", "style")],
)
def on_dropdown_level_1_value(value_level_1, level_2_style):
    options = []
    style = level_2_style.copy()
    if value_level_1 is not None:
        options = oc.get_level_2_dropdown_items(value_level_1)
        style["display"] = "block"
    else:
        style["display"] = "none"
    return style, options, None


@app.callback(
    [Output("entity-choice-selected-entity", "children"), Output("button-to-dashboard", "style")],
    [Input("dropdown-entity-choice-level-1", "value"), Input("dropdown-entity-choice-level-2", "value")],
    [State("button-to-dashboard", "style")],
)
def on_set_value_level_1_level_2(value_level_1, value_level_2, button_to_dashboard_style):
    if value_level_1 is not None:
        if value_level_2 is not None:
            button_to_dashboard_style["display"] = "block"
            return ";".join((value_level_1, value_level_2)), button_to_dashboard_style
    return None, button_to_dashboard_style
