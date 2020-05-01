import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from app import app

layout = html.Div(id="div-data-chorus-dt")


@app.callback(Output("div-data-chorus-dt", "children"), [Input("selected-entity", "children")])
def display_graphs(selected_entity):
    organisation, service = selected_entity.split(";")
    return organisation + " / " + service
