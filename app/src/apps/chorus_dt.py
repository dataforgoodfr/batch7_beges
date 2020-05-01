import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Output, Input, State

from app import app
from utils.chorus_dt_handler import ch
from components.html_components import build_figure_container
from components.figures_templates import xaxis_format

def make_donut_by_prestation():
    """
        Render and update a donut figure to show emissions distribution by prestation type
    """

    # Load chorus dt data based on chosen code_structure
    # TODO: improve and standardize data import logic
    chorus_dt_df = ch.get_structure_data(code_structure=None)
    prestation_df = chorus_dt_df.groupby(['prestation_type'])['cumulative_distance'].sum().reset_index()
    fig = go.Figure(
        data=[go.Pie(labels=prestation_df.prestation_type, values=prestation_df['cumulative_distance'], hole=.3)])
    fig.update_layout(plot_bgcolor='white', template='plotly_white', margin={'t': 30, 'r': 30, 'l': 30})
    return fig

def make_emissions_timeseries():
    """
        Render and update a barplot figure to show emissions evolution with time
    """

    # Load chorus dt data based on chosen code_structure
    # TODO: improve and standardize data import logic
    chorus_dt_df = ch.get_structure_data(code_structure=None)
    timeseries_df = chorus_dt_df.groupby(['mission_start_month'], as_index=False)['cumulative_distance'].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeseries_df['mission_start_month'], y=timeseries_df['cumulative_distance'].values, \
                             mode='lines+markers', line=dict(width=3)))
    fig.update_layout(plot_bgcolor='white', template='plotly_white', margin={'t': 30, 'r': 30, 'l': 30},\
                      xaxis=xaxis_format
                      )
    return fig

select_prestation_type = dcc.Dropdown(
    id='select-prestation_type',
    options=[{'label': 'Train', 'value': 'T'}, {'label': 'Avion', 'value': 'A'}]
)

card_indicateur = dbc.Card(dbc.CardBody([
    html.H3("Nombre de trajets"),
    html.H3('2 300')
]), className='pretty_container')

def make_card_indicateur(title, value):
    return dbc.Card(dbc.CardBody([
        html.P(title),
        html.H3(value)
    ]), className='pretty_container')

cards = dbc.CardDeck([
    make_card_indicateur("Nombre de trajets", "2 300"),
    make_card_indicateur("Emissions (eCO2)", "2M"),
    make_card_indicateur("Indicateur X", "XX"),
    make_card_indicateur("Indicateur Y", "YY"),
])

layout = html.Div([
    dbc.Row(html.P('', id='values-selected')),
    # Cards row
    dbc.Row([
        dbc.Col([
                html.B('', id='selected-entity-show'),
                dbc.Card(dbc.CardBody([
                    html.H3('Filtres'),
                    html.Br(),
                    dbc.FormGroup([
                        dbc.Label("Type de prestation"),
                        select_prestation_type
                    ])

                ]), className='pretty_container'),
                dbc.Card(dbc.CardBody([
                    html.H3('Exporter les données'),
                    html.Br(),
                    dbc.Button('Export', id='export')
                ]), className='pretty_container'),
                dbc.Jumbotron("Explications sur les graphiques et leur fonctionnement..."),
        ]),
        dbc.Col([
            cards,
            build_figure_container(title='Évolution temporelles des émissions', id='timeseries-chorus-dt', \
                                   footer='Explications..'),
        ], width=9)
    ]),
    dbc.Row([
        dbc.Col([
            build_figure_container(title='Histogramme ', id='hist-by-distance', \
                                   footer='Explications..'),
        ], width=8),
        dbc.Col([
            build_figure_container(title='Répartition des émissions par type de déplacement', id='donut-by-prestation', \
                                   footer='Explications..'),
        ], width=4),

    ])
], id="div-data-chorus-dt")

@app.callback(
    Output("selected-entity-show", "children"), [Input("selected-entity", "children")]
)
def on_selected_entity_fill_tabs_data(selected_entity):
    if selected_entity is not None:
        organisation, service = selected_entity.split(";")
        return "Organisation : " + organisation + ", Service : " + service
    else:
        return "empty"

@app.callback(Output("values-selected'", "children"), [Input("selected-entity", "children")])
def display_graphs(selected_entity):
    organisation, service = selected_entity.split(";")
    return organisation + " / " + service


@app.callback(
    Output("timeseries-chorus-dt", "figure"), [Input("selected-entity", "children")]
)
def update_emissions_timeseries(selected_entity):
    return make_emissions_timeseries()


@app.callback(
    Output("donut-by-prestation", "figure"), [Input("selected-entity", "children")]
)
def update_donut_by_prestation(selected_entity):
    return make_donut_by_prestation()