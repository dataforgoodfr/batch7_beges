import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from app import app
from utils.organization_chart import oc
from utils.chorus_dt_handler import ch
from components.html_components import build_figure_container, build_card_indicateur
from components.figures_templates import xaxis_format


# TODO: move make figure function to chorus_dt_components.py in components
def get_donut_by_prestation_type(code_structure=None):
    """
        Render and update a donut figure to show emissions distribution by prestation type
    """
    # Load chorus dt data based on chosen code_structure
    # TODO: improve and standardize data import logic
    chorus_dt_df = ch.get_structure_data(code_structure)
    prestation_df = chorus_dt_df.groupby(["prestation_type"])["distance"].sum().reset_index()
    fig = go.Figure(data=[go.Pie(labels=prestation_df.prestation_type, values=prestation_df["distance"], hole=0.3)])
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


def get_emissions_timeseries(code_structure=None):
    """
        Render and update a barplot figure to show emissions evolution with time
    """
    # Load chorus dt data based on chosen code_structure
    # TODO: improve and standardize data import logic
    chorus_dt_df = ch.get_structure_data(code_structure)
    chorus_dt_df["year_month"] = chorus_dt_df["date_debut_mission"].dt.to_period("M")
    timeseries_df = chorus_dt_df.groupby(["year_month"])["distance"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=timeseries_df["year_month"].astype(str),
            y=timeseries_df["distance"].values,
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
        build_card_indicateur("Nombre de trajets", "2 300"),
        build_card_indicateur("Emissions (eCO2)", "2M"),
        build_card_indicateur("Indicateur X", "XX"),
        build_card_indicateur("Indicateur Y", "YY"),
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
                        build_figure_container(
                            title="Répartition des émissions par type de déplacement",
                            id="donut-by-prestation",
                            footer="Explications..",
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


@app.callback(Output("timeseries-chorus-dt", "figure"), [Input("dashboard-selected-entity", "children")])
def update_emissions_timeseries(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    return get_emissions_timeseries(service.code_chorus)


@app.callback(Output("donut-by-prestation", "figure"), [Input("dashboard-selected-entity", "children")])
def update_donut_by_prestation(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    return get_donut_by_prestation_type(service.code_chorus)
