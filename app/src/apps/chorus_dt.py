import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State

from app import app
from utils.organization_chart import oc
from utils.chorus_dt_handler import ch
from components.html_components import build_figure_container, build_card_indicateur
from components.figures_templates import xaxis_format

# TODO: move make figure function to chorus_dt_components.py in components
def get_donut_by_prestation_type(df):
    """
        Render and update a donut figure to show emissions distribution by prestation type
    """
    prestation_df = df.groupby(["prestation_type"])["CO2e/trip"].sum().reset_index()
    print(df.shape)
    fig = go.Figure(data=[go.Pie(labels=prestation_df.prestation_type, values=prestation_df["CO2e/trip"], hole=0.3)])
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
                        html.B("", id="selected-entity-show"),
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


@app.callback(Output("selected-entity-show", "children"), [Input("selected-entity", "children")])
def on_selected_entity_fill_tabs_data(selected_entity):
    if selected_entity is not None:
        organization, service = oc.get_organization_service(selected_entity)
        return "Organisation : " + organization.label + ", Service : " + service.label
    else:
        return "empty"


@app.callback(
    [Output("donut-by-prestation", "figure"), Output("timeseries-chorus-dt", "figure"),],
    [Input("selected-entity", "children")],
)
def update_graphs(selected_entity):
    organization, service = oc.get_organization_service(selected_entity)
    chorus_dt_df = ch.get_structure_data(service.code_chorus).copy()

    return [get_donut_by_prestation_type(chorus_dt_df), get_emissions_timeseries(chorus_dt_df)]
