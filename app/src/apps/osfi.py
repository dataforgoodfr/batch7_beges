import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

from app import app
from utils.organization_chart import oc
from utils.osfi_handler import oh
from dash.dependencies import Input, State, Output

from components.html_components import build_figure_container


def get_pie(data, column):
    fig = go.Figure(data=[go.Pie(labels=data["Nom du bien"], values=data[column], hole=0.3)])
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


layout = html.Div(
    [
        # dbc.Row([dbc.Col([html.B("", id="osfi-selected-entity-show"),]),]),
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Emission electricité par batiment", id="emission-electricity-pie", footer="Explications..."
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Emission gaz par batiment", id="emission-gas-pie", footer="Explications..."
                ),
                width=12,
            )
        ),
    ]
)


@app.callback(Output("osfi-selected-entity-show", "children"), [Input("selected-entity", "children")])
def on_selected_entity_fill_tabs_data(lntity):
    if selected_entity is not None:
        organization, service = oc.get_organization_service(selected_entity)
        return "Organisation : " + organization.label + ", Service : " + service.label
    else:
        return "empty"


@app.callback(
    [Output("emission-electricity-pie", "figure"), Output("emission-gas-pie", "figure")],
    [Input("selected-entity", "children")],
)
def update_graphs(selected_entity):
    organization, service = oc.get_organization_service(selected_entity)
    data = oh.get_structure_data(service.code_osfi)
    print(data)
    electricity_pie_graph = get_pie(data, "emission_electricity")
    gas_pie_graph = get_pie(data, "emission_gaz")
    return electricity_pie_graph, gas_pie_graph
