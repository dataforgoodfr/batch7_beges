import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

import plotly.graph_objects as go

from app import app
from utils.organization_chart import oc
from utils.osfi_handler import oh
from dash.dependencies import Input, State, Output

from components.html_components import build_figure_container, build_table_container


def get_pie(data, column):
    fig = go.Figure(data=[go.Pie(labels=data["Nom du bien"], values=data[column], hole=0.3)])
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig

def get_emissions_timeseries(data, column):
    biens = data["Nom du bien"].unique()
    fig = go.Figure()
    for bien in biens:
        plot_data = data.loc[data["Nom du bien"] == bien]
        fig.add_trace(
            go.Scatter(name=bien,
                x=plot_data["Date"].astype(str),
                y=plot_data[column].values,
                mode="lines+markers",
                line=dict(width=3),
            )
    )
    fig.update_layout(
        plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30}#, xaxis=xaxis_format
    )
    return fig


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                build_table_container(
                    title="Liste de biens", id="osfi-all-data-table", footer="Explications..."
                ),
                width=12,
            )
        ),
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
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Évolution temporelles des émissions (électricité)", id="electricity_time_series", footer="Explications..."
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Évolution temporelles des émissions (gaz)", id="gaz_time_series", footer="Explications..."
                ),
                width=12,
            )
        ),
    ]
)


@app.callback(
    [
        Output("osfi-all-data-table", "columns"),
        Output("osfi-all-data-table", "row_selectable"),
        Output("osfi-all-data-table", "style_data"),
        Output("osfi-all-data-table", "style_cell_conditional"),
        Output("osfi-all-data-table", "data"),
    ],
    [Input("dashboard-selected-entity", "children")],
)

def update_graphs(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    data = oh.get_structure_data(service.code_osfi)
    columns_to_keep = ["Nom du bien", "Building type", "Adresse", "Code postal", "Ville", "Departement"]
    columns = [{"name": i, "id": i} for i in columns_to_keep]
    row_selectable = "multi"
    selected_rows=[]
    style_data={'whiteSpace': 'normal','height': 'auto','minWidth': '60px', 'width': '180px', 'maxWidth': '180px'}
    style_cell_conditional =[{'if': {'column_id': i}, 'textAlign': 'left'} for i in ['Nom du bien','Date']]
    data_to_return = data.to_dict("records")
    return columns, row_selectable, style_data, style_cell_conditional, data_to_return


@app.callback(
    [
        Output("emission-electricity-pie", "figure"),
        Output("emission-gas-pie", "figure"),
        Output("electricity_time_series", "figure"),
        Output("gaz_time_series", "figure"),
    ],
    [
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-all-data-table", "data"),
    ],
    )
def update_graphs_selected(selected_rows, data):
    if selected_rows is None:
        selected_rows = []
    selected_rows = [data[int(i)] for i in selected_rows]
    selected_rows = pd.DataFrame(selected_rows)
    data = pd.DataFrame(data)
    if len(selected_rows) > 0:
        electricity_pie_graph = get_pie(selected_rows, "emission_electricity")
        gas_pie_graph = get_pie(selected_rows, "emission_gaz")
        electricity_time_series = get_emissions_timeseries(selected_rows, "emission_electricity")
        gaz_time_series = get_emissions_timeseries(selected_rows, "emission_gaz")
    else: 
        electricity_pie_graph = get_pie(pd.DataFrame(data), "emission_electricity")
        gas_pie_graph = get_pie(pd.DataFrame(data), "emission_gaz")
        electricity_time_series = get_emissions_timeseries(data, "emission_electricity")
        gaz_time_series = get_emissions_timeseries(data, "emission_gaz")
    return electricity_pie_graph, gas_pie_graph, electricity_time_series, gaz_time_series
