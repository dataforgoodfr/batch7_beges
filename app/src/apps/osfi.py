import time
import datetime
import locale

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd

import plotly.graph_objects as go

from app import app, cache
from utils.organization_chart import oc
from utils.osfi_handler import oh
from dash.dependencies import Input, Output, State

from components.html_components import build_figure_container, build_table_container

locale.setlocale(locale.LC_TIME, "")


TIMEOUT = 600


@cache.memoize(timeout=TIMEOUT)
def get_data(selected_entity, selected_rows, buildings, slider_values):
    print("Getting data")
    min_date = unix_to_date(slider_values[0])
    max_date = unix_to_date(slider_values[1])
    entity = oc.get_entity_by_id(selected_entity)
    data = oh.get_structure_data(entity.code_osfi)
    # If no rows are selected, we are displaying all of them
    # Might seem a bit conter intuitive.
    if selected_rows is None or len(selected_rows) == 0:
        data_to_display = pd.DataFrame(data)
    else:
        biens = [buildings[int(i)] for i in selected_rows]
        biens = pd.DataFrame(biens)
        codes = biens["Nom du bien"]
        data_to_display = data[data["Nom du bien"].isin(codes)]
        data_to_display = pd.DataFrame(data_to_display)
    data_to_display = data_to_display[data_to_display["Date"] >= pd.Timestamp(min_date)]
    data_to_display = data_to_display[data_to_display["Date"] <= pd.Timestamp(max_date)]
    return data_to_display


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
            go.Scatter(
                name=bien,
                x=plot_data["Date"].astype(str),
                y=plot_data[column].values,
                mode="lines+markers",
                line=dict(width=3),
            )
        )
    fig.update_layout(
        plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30}  # , xaxis=xaxis_format
    )
    return fig


def get_building_location(buildings):
    data = [go.Scattermapbox(lon=buildings["longitude RT"], lat=buildings["Latitude RT"])]
    center = {"lon": buildings["longitude RT"].mean(), "lat": buildings["Latitude RT"].mean()}
    center = {
        "lon": (buildings["longitude RT"].max() + buildings["longitude RT"].min()) / 2.0,
        "lat": (buildings["Latitude RT"].max() + buildings["Latitude RT"].min()) / 2.0,
    }
    zoom = 5.0 / max(
        buildings["longitude RT"].max() - buildings["longitude RT"].min(),
        buildings["Latitude RT"].max() - buildings["Latitude RT"].min(),
    )
    print(zoom)

    layout = dict(
        geo=go.layout.Geo(
            scope="world",
            fitbounds="locations",
            # showframe=True,
            # showlakes=False,
            # lakecolor="lightblue",
            # showocean=False,
            # oceancolor="lightblue",
            # showrivers=True,
            # rivercolor="lightblue",
            # riverwidth=1,
            # showland=True,
            # landcolor="gainsboro",
            # showcoastlines=False,
            # coastlinewidth=0.5,
            # showcountries=True,
            # countrycolor="darkgray",
            # countrywidth=0.5,
        ),
        # mapbox=dict(style="carto-positron", center=center, zoom=zoom),
        mapbox=dict(style="open-street-map", center=center, zoom=zoom),
        margin=dict(r=0, l=0, t=0, b=0),
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_geos(fitbounds="locations")
    return fig


def unix_time_millis(dt):
    """ Convert datetime to unix timestamp """
    return int(time.mktime(dt.timetuple()))


def unix_to_date(unix):
    """ Convert unix timestamp to datetime. """
    return datetime.date.fromtimestamp(unix)


def get_marks(dates):
    """ Returns the marks for labeling.
        Every Nth value will be used.
    """
    result = {}
    for i, date in enumerate(dates):
        result[unix_time_millis(date)] = dict(label="")
    result[unix_time_millis(dates[0])]["label"] = dates[0].strftime("%b %Y")
    result[unix_time_millis(dates[-1])]["label"] = dates[-1].strftime("%b %Y")

    return result


filters = dbc.Card(
    [
        dbc.CardHeader(html.H4("Filtres")),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id="osfi-dates-rangeslider-min-display"),
                            width={"size": 3, "offset": 1},
                            style={"text-align": "left"},
                        ),
                        dbc.Col(
                            html.Div(id="osfi-dates-rangeslider-max-display"),
                            width={"size": 3, "offset": 4},
                            style={"text-align": "right"},
                        ),
                    ]
                ),
                dcc.RangeSlider(id="osfi-dates-rangeslider"),
            ]
        ),
    ],
    className="m-2 pretty_container",
)
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Jumbotron(
                        [
                            html.P(
                                "Les consommations sont extraites de la base de données de l'outil OSFI (deepki) et les facteurs d'émissions appliqués sont 0.0571 kgCO2e/kWh pour l'électricité, et 0.227 kgCO2/ kWh pour le gaz."
                            ),
                            html.P(dbc.Button("En savoir plus", color="primary", href="/methodologie")),
                        ]
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [filters, build_table_container(title="Liste de biens", id="osfi-all-data-table")],
                    width=6,
                    style={"textAlign": "left"},
                ),
                dbc.Col(
                    build_figure_container(title="Carte des biens", id="osfi-building-location"),
                    width=6,
                    style={"textAlign": "left"},
                ),
            ]
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
                    title="Évolution temporelles des émissions (électricité)",
                    id="electricity_time_series",
                    footer="Explications...",
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Évolution temporelles des émissions (gaz)", id="gas_time_series", footer="Explications..."
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
        Output("osfi-all-data-table", "hidden_columns"),
        Output("osfi-all-data-table", "data"),
    ],
    [Input("dashboard-selected-entity", "children")],
)
def fill_dash_table_with_buildings(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    data = oh.get_structure_data(service.code_osfi)
    columns_to_keep = ["Nom du bien", "Building type", "Adresse", "Code postal", "Ville", "Departement"]
    columns = [{"name": i, "id": i} for i in columns_to_keep]
    hidden_columns = []
    for c in columns:
        if c["name"] != "Nom du bien":
            c["hideable"] = True
            hidden_columns.append(c["id"])
    row_selectable = "multi"
    buildings = data[columns_to_keep].drop_duplicates()
    data_to_return = buildings.to_dict("records")
    return columns, row_selectable, hidden_columns, data_to_return


@app.callback(
    [
        Output("osfi-dates-rangeslider", "min"),
        Output("osfi-dates-rangeslider", "max"),
        Output("osfi-dates-rangeslider", "marks"),
        Output("osfi-dates-rangeslider", "value"),
    ],
    [Input("dashboard-selected-entity", "children")],
)
def set_slider_range(selected_entity):
    service = oc.get_entity_by_id(selected_entity)
    data = oh.get_structure_data(service.code_osfi)
    min_date = data["Date"].min()
    max_date = data["Date"].max()
    datelist = pd.date_range(start=min_date, end=max_date, freq="M").to_list()
    marks = get_marks(datelist)
    min_value = unix_time_millis(min_date)
    max_value = unix_time_millis(max_date)
    return min_value, max_value, marks, [min_value, max_value]


@app.callback(
    [
        Output("osfi-dates-rangeslider-min-display", "children"),
        Output("osfi-dates-rangeslider-max-display", "children"),
    ],
    [Input("osfi-dates-rangeslider", "value")],
)
def update_sliders_min_max_display(range_slider_value):
    min_display = unix_to_date(range_slider_value[0]).strftime("%b %Y")
    max_display = unix_to_date(range_slider_value[1]).strftime("%b %Y")
    return min_display, max_display


@app.callback(
    Output("emission-electricity-pie", "figure"),
    [
        Input("dashboard-selected-entity", "children"),
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-all-data-table", "data"),
        Input("osfi-dates-rangeslider", "value"),
    ],
)
def update_emission_electricity_pie(selected_entity, selected_rows, buildings, slider_values):
    t1 = time.time()
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    t2 = time.time()
    electricity_pie_graph = get_pie(data_to_display, "emission_electricity")
    return electricity_pie_graph


@app.callback(
    Output("emission-gas-pie", "figure"),
    [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_gas_pie(selected_rows, slider_values, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    gas_pie_graph = get_pie(data_to_display, "emission_gaz")
    return gas_pie_graph


@app.callback(
    Output("electricity_time_series", "figure"),
    [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_electricity_time_series(selected_rows, slider_values, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    electricity_time_series = get_emissions_timeseries(data_to_display, "emission_electricity")
    return electricity_time_series


@app.callback(
    Output("gas_time_series", "figure"),
    [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_gas_time_series(selected_rows, slider_values, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    gas_time_series = get_emissions_timeseries(data_to_display, "emission_gaz")

    return gas_time_series


@app.callback(
    Output("osfi-building-location", "figure"),
    [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_map_location(selected_rows, slider_values, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    buildings = data_to_display.groupby("Nom du bien").first()
    return get_building_location(buildings)
