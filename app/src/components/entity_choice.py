import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from utils.entity_handler import EntityHandler

eh = EntityHandler()
print(eh.get_level_1_dropdown_items())
level_2_style = {"margin": "10px", "display": "none"}

layout = html.Div(
    id="div-entity-choice",
    children=[
        dcc.Dropdown(
            id="dropdown-entity-choice-level-1",
            options=eh.get_level_1_dropdown_items(),
            placeholder="Choisissez votre organisation",
            style={"margin": "10px"},
        ),
        dcc.Dropdown(id="dropdown-entity-choice-level-2", placeholder="Choisissez votre service", style=level_2_style),
        html.Div(id="selected-entity", style={"display": "none"}),
    ],
)


def register_callbacks(app):
    @app.callback(
        [
            Output("dropdown-entity-choice-level-2", "style"),
            Output("dropdown-entity-choice-level-2", "options"),
            Output("selected-entity", "children"),
        ],
        [Input("dropdown-entity-choice-level-1", "value"), Input("dropdown-entity-choice-level-2", "value")],
    )
    def on_dropdown_level_1_value(value_level_1, value_level_2):
        options = []
        style = level_2_style
        selected_entity = None
        if value_level_1 is not None:
            if value_level_2 is None:
                if value_level_1 != "AC":
                    options = eh.get_level_2_dropdown_items(value_level_1)
                    style = level_2_style.copy()
                    style["display"] = "block"
                elif value_level_1 == "AC":
                    selected_entity = "AC;"
            else:
                options = eh.get_level_2_dropdown_items(value_level_1)
                style = level_2_style.copy()
                style["display"] = "block"
                selected_entity = ";".join((value_level_1, value_level_2))
        return style, options, selected_entity
