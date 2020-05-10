import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State
import numpy as np

from app import app
from utils.organization_chart import oc
from utils.chorus_dt_handler import ch
from components.html_components import build_figure_container, build_card_indicateur
from components.figures_templates import xaxis_format


# TODO: move get figure function to chorus_dt_components.py in components
# TODO:
# - List of top trips based on emissions
# - Emissions
# - Nombre des trajets train vs avions


def get_kpi_emissions(df):
    return "{:,} kg".format(int(np.round(df["CO2e/trip"].sum(), 0))).replace(",", " ")


def get_kpi_emissions_example(df, example_ec02=0.11):
    return "{:,}".format(int(np.round((df["CO2e/trip"].sum() / example_ec02), 0))).replace(",", " ")


def get_kpi_distance(df):
    return "{:,} km".format(int(np.round(df["distance"].sum(), 0))).replace(",", " ")  # In km


def get_kpi_trips_count(df):
    return "{:,}".format(int(np.round(df["distance"].count(), 0))).replace(",", " ")

def get_donut_by_prestation_type(df):
    """
        Render and update a donut figure to show emissions distribution by prestation type
    """
    prestation_df = df.groupby(["prestation"])["CO2e/trip"].sum().reset_index()
    fig = go.Figure(data=[go.Pie(labels=prestation_df.prestation, values=prestation_df["CO2e/trip"], hole=0.3)])
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


def get_hist_by_distance_group(df):
    """
        Render and update a donut figure to show emissions distribution by prestation type
    """
    distance_df = df.groupby(["distance_group", "prestation"])["CO2e/trip"].sum().reset_index()
    distance_df = distance_df.pivot(index="distance_group", columns="prestation", values="CO2e/trip")
    fig = go.Figure()
    for col in distance_df.columns:
        fig.add_trace(go.Bar(x=distance_df.index, y=distance_df[col], name=col))
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


def get_emissions_timeseries(df):
    """
        Render and update a scatter plot figure to show emissions evolution with time
    """
    timeseries_df = df.groupby(["year_month"])["CO2e/trip"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=timeseries_df["year_month"].astype(str),
            y=timeseries_df["CO2e/trip"].values,
            mode="lines+markers",
            line=dict(width=3),
        )
    )
    fig.update_layout(
        plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30}, xaxis=xaxis_format
    )
    return fig


select_prestation_type = dcc.Dropdown(
    id="select-prestation_type", options=[{"label": "Train", "value": "T"}, {"label": "Avion", "value": "A"}]
)


cards = dbc.CardDeck(
    [
        build_card_indicateur("Emissions (kg eqCO2)", "0", "kpi-emissions"),
        build_card_indicateur("Emissions (# Tasses de café)", "0", "kpi-emissions-example"),
        build_card_indicateur("Nombre de trajets", "0", "kpi-trips"),
        build_card_indicateur("Distance totale (km)", "0", "kpi-distance"),
    ]
)

layout = html.Div(
    [
        dbc.Row(html.P("", id="values-selected")),
        # Cards row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Filtres"),
                                    html.Br(),
                                    dbc.FormGroup([dbc.Label("Type de prestation"), select_prestation_type]),
                                ]
                            ),
                            className="pretty_container",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [html.H3("Exporter les données"), html.Br(), dbc.Button("Export", id="export")]
                            ),
                            className="pretty_container",
                        ),
                        dbc.Jumbotron("Explications sur les graphiques et leur fonctionnement..."),
                    ]
                ),
                dbc.Col(
                    [
                        cards,
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        build_figure_container(
                                            title="Répartition des émissions par type de déplacement",
                                            id="donut-by-prestation",
                                            footer="Explications..",
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        build_figure_container(
                                            title="Répartition des émissions par distance de trajet",
                                            id="hist-by-distance",
                                            footer="Explications..",
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=9,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        build_figure_container(
                            title="Évolution temporelles des émissions",
                            id="timeseries-chorus-dt",
                            footer="Explications..",
                        )
                    ],
                    width=12,
                )
            ]
        ),
    ],
    id="div-data-chorus-dt",
)


@app.callback(
    [
        Output("kpi-emissions", "children"),
        Output("kpi-emissions-example", "children"),
        Output("kpi-trips", "children"),
        Output("kpi-distance", "children"),
        Output("donut-by-prestation", "figure"),
        Output("hist-by-distance", "figure"),
        Output("timeseries-chorus-dt", "figure"),
    ],
    [Input("selected-entity", "children")],
)
def update_graphs(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    chorus_dt_df = ch.get_structure_data(service.code_chorus).copy()

    return [
        get_kpi_emissions(chorus_dt_df),
        get_kpi_emissions_example(chorus_dt_df),
        get_kpi_trips_count(chorus_dt_df),
        get_kpi_distance(chorus_dt_df),
        get_donut_by_prestation_type(chorus_dt_df),
        get_hist_by_distance_group(chorus_dt_df),
        get_emissions_timeseries(chorus_dt_df),
    ]
