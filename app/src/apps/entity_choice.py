import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from utils.organization_chart import oc
from app import app


layout = html.Div(
    id="div-entity-choice",
    children=[
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
        html.Div(id="selected-entity", style={"display": "none"}),
    ],
)


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
    if value_level_1 is not None:
        if value_level_1 != "AC":
            options = oc.get_level_2_dropdown_items(value_level_1)
            style = level_2_style.copy()
            level_2_style["display"] = "block"
        else:
            level_2_style["display"] = "none"
    else:
        level_2_style["display"] = "none"
    return level_2_style, options, None


@app.callback(
    Output("selected-entity", "children"),
    [Input("dropdown-entity-choice-level-1", "value"), Input("dropdown-entity-choice-level-2", "value")],
)
def on_set_value_level_1_level_2(value_level_1, value_level_2):
    if value_level_1 is not None:
        if value_level_1 == "AC":
            return "AC;"
        if value_level_2 is not None:
            return ";".join((value_level_1, value_level_2))
    return None
