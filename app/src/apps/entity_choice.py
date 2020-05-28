import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from dash.dependencies import Output, Input, State, ALL

from utils.organization_chart import oc
from app import app


def get_dropdown(parent_id="root", depth=1):
    return dcc.Dropdown(
        id={"type": "entity-choice-dropdown-level", "id": depth},
        options=oc.get_children_dropdown_items(parent_id),
        placeholder="Choisissez votre entité de niveau %s" % depth,
        className="mb-3",
        clearable=True,
    )


layout = html.Div(
    id="div-entity-choice",
    children=[
        html.Div(id="entity-choice-div-url-redirect-to-dashboard", style={"display": "none"}),
        html.Div(id="entity-choice-selected-entity", style={"display": "none"}),
        dbc.Row(
            dbc.Col(
                [html.H1("Choisissez votre entité"), dbc.Form([get_dropdown()], id="entity-choice-dropdowns")],
                width={"size": 6, "offset": 3},
            )
        ),
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
        entity = oc.get_entity_by_id(selected_entity)
        return dcc.Location(id="url-redirect-to-dashboard", pathname="/tableau_de_bord/%s" % entity.id)


@app.callback(
    Output("button-to-dashboard", "style"),
    [Input("entity-choice-selected-entity", "children")],
    [State("button-to-dashboard", "style")],
)
def toggle_button_if_selected_entity(selected_entity, button_to_dashboard_style):
    if selected_entity:
        button_to_dashboard_style["display"] = "block"
    else:
        button_to_dashboard_style["display"] = "none"
    return button_to_dashboard_style


@app.callback(
    [Output("entity-choice-dropdowns", "children"), Output("entity-choice-selected-entity", "children")],
    [Input({"type": "entity-choice-dropdown-level", "id": ALL}, "value")],
    [State("entity-choice-dropdowns", "children")],
)
def add_dropdown(values, dropdowns):
    ctx = dash.callback_context
    ctx_msg = json.dumps({"states": ctx.states, "triggered": ctx.triggered, "inputs": ctx.inputs}, indent=2)
    selected_entity = None
    if not ctx.triggered:
        raise PreventUpdate
    else:
        depth = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["id"]
        # We delete the decedents dropdowns of the current changed value
        dropdowns = dropdowns[:depth]

        entity_id = ctx.triggered[0]["value"]
        # The value can be None if the dropdown is cleared
        if entity_id:
            entity = oc.get_entity_by_id(entity_id)
            # If there are some children, we add a dropdown with the children choices
            if entity.children:
                dropdowns.append(get_dropdown(parent_id=entity_id, depth=entity.depth + 1))
            # Else, we set the selected_entity with the selected value
            else:
                selected_entity = entity.id

    return dropdowns, selected_entity
