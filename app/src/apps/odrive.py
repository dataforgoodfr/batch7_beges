import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from app import app
from utils.organization_chart import oc
from utils.odrive_handler import ov
from components.html_components import build_figure_container, build_card_indicateur


def get_donut_by_entity_type(code_structure=None):
    odrive_df = ov.get_structure_data(code_structure)
    prestation_df = odrive_df.groupby(["Entité 3"])["Emissions (g/an)"].sum().reset_index()
    prestation_df.entities = list(set(odrive_df["Entité 3"]))
    fig = go.Figure(data=[go.Pie(labels=prestation_df["Entité 3"], values=prestation_df["Emissions (g/an)"], hole=0.3)])
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


cards = dbc.CardDeck(
    [
        build_card_indicateur("Nombre de véhicules", "XX"),
        build_card_indicateur("Emissions (CO2)", "YY"),
        build_card_indicateur("Indicateur X", "XX"),
        build_card_indicateur("Indicateur Y", "YY"),
    ]
)


select_odrive_vehicle_type = dcc.Dropdown(
    id="select_odrive_vehicle_type",
    options=[
        {"label": "Electrique", "value": "E"},
        {"label": "Essence", "value": "F"},
        {"label": "Diesel", "value": "D"},
    ],
)

layout = html.Div(
    [
        # Cards row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.B("", id="selected-odrive-vehicle_type"),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Filtres"),
                                    html.Br(),
                                    dbc.FormGroup(
                                        [dbc.Label("Selectionner Type véhicule"), select_odrive_vehicle_type]
                                    ),
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
                            title="Répartition par direction", id="donut-by-entity", footer="Explications.."
                        ),
                    ],
                    width=9,
                ),
            ]
        )
    ],
    id="div-data-odrive",
)


@app.callback(Output("donut-by-entity", "figure"), [Input("dashboard-selected-entity", "children")])
def update_donut_by_prestation(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    return get_donut_by_entity_type(service.code_odrive)
