import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from utils.entity_handler import EntityHandler

eh = EntityHandler()
print(eh.get_level_1_dropdown_items())

layout = html.Div(
    id="div-entity-choice",
    children=[
        dcc.Dropdown(
            id="dropdown-entity-choice-level-1",
            options=eh.get_level_1_dropdown_items(),
            # value=eh.get_level_1_dropdown_items()[0]["value"],
            placeholder="Choisissez votre organisation",
            style={"margin": "10px"},
        ),
        dcc.Dropdown(
            id="dropdown-entity-choice-level-2", placeholder="Choisissez votre service", style={"margin": "10px"}
        ),
        html.Div(
            id="div-selected-entity",
            children=[html.P("Vous avez selectionné : "), html.P(id="p-selected-entity"),],
            style={"display": " inline-block"},
        ),
    ],
)


def register_callbacks(app):
    @app.callback(
        [Output("dropdown-entity-choice-level-2", "options"), Output("dropdown-entity-choice-level-2", "value"),],
        [Input("dropdown-entity-choice-level-1", "value")],
    )
    def change_dropdown_level_2_options(value):
        if value is not None:
            options = eh.get_level_2_dropdown_items(value)
            level_2_value = options[0]["value"]
        else:
            options = []
            level_2_value = None
        return options, level_2_value

    @app.callback(
        Output("p-selected-entity", "children"),
        [Input("dropdown-entity-choice-level-1", "value"), Input("dropdown-entity-choice-level-2", "value"),],
    )
    def display_selected_entity(level_1, level_2):
        if level_1 is None:
            level_1_label = ""
        else:
            level_1_label = eh.get_level_1_label(level_1)
        if level_2 is None:
            level_2_label = ""
        else:
            level_2_label = eh.get_level_2_label(level_2)
        return level_1_label + " / " + level_2_label
