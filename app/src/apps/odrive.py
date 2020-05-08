import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State

from app import app
from utils.organization_chart import oc
from utils.odrive_handler import ov
from components.html_components import build_figure_container, build_card_indicateur
from components.figures_templates import xaxis_format

# TODO: move make figure function to chorus_dt_components.py in components
def get_donut_by_prestation_type(code_structure=None):
    odrive_df = ov.get_structure_data(code_structure)
    prestation_df = odrive_df.groupby(["Entité 3"])["Emissions (g/an)"].sum().reset_index()
    prestation_df.entities = list(set(odrive_df["Entité 3"]))
    fig = go.Figure(
        data=[go.Pie(labels=prestation_df.prestation_type, values=prestation_df["Emissions (g/an)"], hole=0.3)]
    )
    fig.update_layout(plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30})
    return fig


cards = dbc.CardDeck(
    [
        build_card_indicateur("Nombre de véhicules", "XX"),
        build_card_indicateur("Emissions (eCO2)", "YY"),
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
    ],
    id="div-data-chorus-dt",
)


@app.callback(Output("donut-by-prestation", "figure"), [Input("selected-entity", "children")])
def update_donut_by_prestation(selected_entity):
    organization, service = oc.get_organization_service(selected_entity)
    return get_donut_by_prestation_type(service.code_chorus)
