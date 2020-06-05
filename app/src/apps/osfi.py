import time
import datetime
import locale

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

from app import app, cache
from utils.organization_chart import oc
from utils.osfi_handler import oh
from dash.dependencies import Input, Output, State

from components.html_components import build_figure_container, build_table_container, build_card_indicateur

locale.setlocale(locale.LC_TIME, "")


TIMEOUT = 600


@cache.memoize(timeout=TIMEOUT)
def get_data(selected_entity, selected_rows, buildings, slider_values):
    entity = oc.get_entity_by_id(selected_entity)
    data = oh.get_structure_data(entity.code_osfi)

    # Start of month for min slider range
    min_date = pd.Timestamp(unix_to_date(slider_values[0])) - pd.offsets.MonthBegin(1)
    max_date = pd.Timestamp(unix_to_date(slider_values[1]))

    # If no rows are selected, we are returning an empty dataframe
    # with the same structure as data
    if selected_rows is None or len(selected_rows) == 0:
        return pd.DataFrame().reindex_like(data)
    else:
        biens = [buildings[int(i)] for i in selected_rows]
        biens = pd.DataFrame(biens)
        codes = biens["Nom du bien"]
        data_to_display = data[data["Nom du bien"].isin(codes)]
        data_to_display = pd.DataFrame(data_to_display)
        data_to_display = data_to_display[data_to_display["Date"] >= min_date]
        data_to_display = data_to_display[data_to_display["Date"] <= max_date]
        return data_to_display


def get_pies(data, data_type: str, unit: str):
    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
        subplot_titles=["Électricité", "Gaz", "Total"],
    )
    data = (
        data.groupby("Nom du bien")[
            [
                oh.column_names[data_type]["gas"],
                oh.column_names[data_type]["electricity"],
                oh.column_names[data_type]["total"],
            ]
        ]
        .sum()
        .reset_index()
    )
    fig.add_trace(
        go.Pie(
            values=data[oh.column_names[data_type]["electricity"]].values,
            labels=data["Nom du bien"],
            scalegroup="one",
            name="Électricité",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Pie(
            labels=data["Nom du bien"],
            values=data[oh.column_names[data_type]["gas"]].values,
            scalegroup="one",
            name="Gaz",
        ),
        1,
        2,
    )
    fig.add_trace(
        go.Pie(
            labels=data["Nom du bien"],
            values=data[oh.column_names[data_type]["total"]].values,
            scalegroup="one",
            name="Total",
        ),
        1,
        3,
    )
    fig.update_traces(
        hole=0.4,
        hoverinfo="label+value+percent+name",
        textposition="inside",
        hovertemplate="%{label}<br>%{value} " + unit + "<br>(%{percent})",
    )
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
    fig.update_layout(plot_bgcolor="white", template="plotly_white")
    return fig


def get_repartition_consumption_pies(data):
    return get_pies(data, "consumption", "kWh")


def get_repartition_emission_pies(data):
    return get_pies(data, "emission", "kgCO2e")


def get_consumption_timeseries(data, display_mode):
    fig = go.Figure()
    data = (
        data.groupby("Date")[[oh.column_names["consumption"]["gas"], oh.column_names["consumption"]["electricity"]]]
        .sum()
        .reset_index()
    )
    if display_mode == "total":
        fig.add_trace(go.Bar(x=data["Date"], y=data[oh.column_names["consumption"]["gas"]], name="Consommation gaz"))
        fig.add_trace(
            go.Bar(
                x=data["Date"], y=data[oh.column_names["consumption"]["electricity"]], name="Consommation électricité"
            )
        )
    elif display_mode == "electricity":
        fig.add_trace(
            go.Bar(
                x=data["Date"], y=data[oh.column_names["consumption"]["electricity"]], name="Consommation électricité"
            )
        )
    elif display_mode == "gas":
        fig.add_trace(go.Bar(x=data["Date"], y=data[oh.column_names["consumption"]["gas"]], name="Consommation gaz"))

    fig.update_layout(
        barmode="relative",
        plot_bgcolor="white",
        showlegend=True,
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},  # , xaxis=xaxis_format
        yaxis=dict(title_text="Consommation en kWh"),
    )
    return fig


def get_emission_timeseries(data, display_mode):
    fig = go.Figure()

    data = (
        data.groupby("Date")[["Emissions de CO2 par l'électricité (kgCO2e)", "Emissions de CO2 par le gaz (kgCO2e)"]]
        .sum()
        .reset_index()
    )
    if display_mode == "total":
        fig.add_trace(go.Bar(x=data["Date"], y=data["Emissions de CO2 par le gaz (kgCO2e)"], name="Emission gaz"))
        fig.add_trace(
            go.Bar(x=data["Date"], y=data["Emissions de CO2 par l'électricité (kgCO2e)"], name="Emission électricité")
        )
    elif display_mode == "electricity":
        fig.add_trace(
            go.Bar(x=data["Date"], y=data["Emissions de CO2 par l'électricité (kgCO2e)"], name="Emission électricité")
        )
    elif display_mode == "gas":
        fig.add_trace(go.Bar(x=data["Date"], y=data["Emissions de CO2 par le gaz (kgCO2e)"], name="Emission gaz"))

    fig.update_layout(
        barmode="relative",
        plot_bgcolor="white",
        showlegend=True,
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},  # , xaxis=xaxis_format
        yaxis=dict(title_text="Emission en kgCO2e"),
    )
    return fig


def get_consumption_timeseries_per_building(data, display_mode):
    # column = "Consumption kwh electricity"
    print(data.columns)
    buildings = data["Nom du bien"].unique()
    fig = go.Figure()
    for building in buildings:
        print("building", building)
        plot_data = data.loc[data["Nom du bien"] == building]
        fig.add_trace(
            go.Scatter(
                name=building,
                x=plot_data["Date"],
                y=plot_data["Consommation d'électricité (kWh)"],
                mode="lines+markers",
                line=dict(width=3),
            )
        )
    fig.update_layout(
        plot_bgcolor="white", template="plotly_white", margin={"t": 30, "r": 30, "l": 30}  # , xaxis=xaxis_format
    )
    return fig


def get_emission_timeseries_per_building(data, display_mode):
    column = "Consumption kwh electricity"
    biens = data["Nom du bien"].unique()
    data = (
        data.groupby("Date")[
            [
                "Emissions de CO2 par l'électricité (kgCO2e)",
                "Emissions de CO2 par le gaz (kgCO2e)",
                "Emissions de CO2 au total (kgCO2e)",
            ]
        ]
        .sum()
        .reset_index()
    )
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


def get_building_location(buildings, data_to_display, selected_rows):
    selected_building_names = [b["Nom du bien"] for i, b in enumerate(buildings) if i in selected_rows]
    building_names_group = data_to_display.groupby("Nom du bien")
    buildings = building_names_group[["Longitude RT", "Latitude RT"]].first()
    markers_sizes = np.log(building_names_group[["Emissions de CO2 par l'électricité (kgCO2e)"]].sum().sum(axis=1))

    def get_marker_color(x):
        if x["Nom du bien"] in selected_building_names:
            return "blue"
        else:
            return "green"

    markers_color = building_names_group[["Nom du bien"]].first().apply(get_marker_color, axis=1).values
    center = {
        "lon": (buildings["Longitude RT"].max() + buildings["Longitude RT"].min()) / 2.0,
        "lat": (buildings["Latitude RT"].max() + buildings["Latitude RT"].min()) / 2.0,
    }
    zoom = 5
    data = [
        dict(
            type="scattermapbox",
            lon=buildings["Longitude RT"],
            lat=buildings["Latitude RT"],
            mode="markers",
            text=building_names_group[["Nom du bien"]].first(),
            marker=dict(size=markers_sizes, color=markers_color),
        )
    ]
    layout = dict(
        geo=go.layout.Geo(scope="world",),
        mapbox=dict(style="open-street-map", center=center, zoom=zoom),
        margin=dict(r=0, l=0, t=0, b=0),
        autosize=True,
        uirevision="no reset of zoom",
    )
    fig = go.Figure(data=data, layout=layout)
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
                dbc.Row(dbc.Col(dcc.RangeSlider(id="osfi-dates-rangeslider", step=None),), className="m-2",),
                dbc.Row(
                    [
                        dbc.Col(html.P("Date de début : "), width=2,),
                        dbc.Col(
                            html.Div(id="osfi-dates-rangeslider-min-display", style={"text-align": "center"}), width=2,
                        ),
                        dbc.Col(
                            dbc.Button(
                                html.I(className="fa fa-chevron-left fa-1x mr-1"),
                                id="osfi-dates-rangeslider-min-down",
                                color="light",
                                block=True,
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Button(
                                html.I(className="fa fa-chevron-right fa-1x mr-1"),
                                id="osfi-dates-rangeslider-min-up",
                                color="light",
                                block=True,
                            ),
                            width=1,
                        ),
                        dbc.Col(html.P("Date de fin : "), width=2),
                        dbc.Col(
                            html.Div(id="osfi-dates-rangeslider-max-display", style={"text-align": "center"}), width=2,
                        ),
                        dbc.Col(
                            dbc.Button(
                                html.I(className="fa fa-chevron-left fa-1x mr-1"),
                                id="osfi-dates-rangeslider-max-down",
                                color="light",
                                block=True,
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dbc.Button(
                                html.I(className="fa fa-chevron-right fa-1x mr-1"),
                                id="osfi-dates-rangeslider-max-up",
                                color="light",
                                block=True,
                            ),
                            width=1,
                        ),
                    ],
                    className="m-2",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Mode d'affichage", html_for="osfi-display-mode-dropdown"), width=2,),
                        dbc.Col(
                            dcc.Dropdown(
                                id="osfi-display-mode-dropdown",
                                options=[
                                    {"label": "Électricité / Gaz", "value": "total"},
                                    {"label": "Électricité", "value": "electricity"},
                                    {"label": "Gaz", "value": "gas"},
                                ],
                                value="total",
                            ),
                            width=10,
                        ),
                    ],
                    className="m-2",
                ),
            ]
        ),
    ],
    className="m-2 pretty_container",
)

# cards = dbc.CardDeck(
# [
# build_card_indicateur("Nombre de bâtiments", "0", "number-of-buildings"),
# build_card_indicateur(", "0", "kilometers_total_odrive"),
# build_card_indicateur("Distance par mois par véhicule (km)", "0", "montly_kilometer_odrive"),
# ]
# )

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
                    width=3,
                ),
                dbc.Col(filters, width=9,),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    build_table_container(title="Liste de biens", id="osfi-all-data-table"),
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
                    title="Répartition de la consommation énergétique par bâtiment",
                    id="osfi-repartition-consumption-pies",
                ),
                width=12,
            ),
        ),
        dbc.Row(
            dbc.Col(
                build_figure_container(
                    title="Répartition des émissions par bâtiment",
                    id="osfi-repartition-emission-pies",
                    footer="Explications...",
                ),
                width=12,
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles de la consommation de gaz par bâtiment (kWh)",
                        id="osfi-consumption-timeseries",
                    ),
                    width=6,
                ),
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles des émissions (kgCO2)", id="osfi-emission-timeseries",
                    ),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles de la consommation par bâtiment (kWh)",
                        id="osfi-consumption-timeseries-per-building",
                    ),
                    width=6,
                ),
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles des émissions par bâtiment (kgCO2)",
                        id="osfi-emission-timeseries-per-building",
                    ),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles de la consommation (kWh)", id="osfi-consumption-timeseries",
                    ),
                    width=6,
                ),
                dbc.Col(
                    build_figure_container(
                        title="Évolution temporelles des émissions (kgCO2)", id="osfi-emission-timeseries",
                    ),
                    width=6,
                ),
            ]
        ),
    ]
)


@app.callback(
    [
        Output("osfi-all-data-table", "columns"),
        Output("osfi-all-data-table", "row_selectable"),
        Output("osfi-all-data-table", "selected_rows"),
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
        if c["name"] not in ["Nom du bien", "Ville"]:
            c["hideable"] = True
            hidden_columns.append(c["id"])
    row_selectable = "multi"
    buildings = data[columns_to_keep].drop_duplicates()
    selected_rows = list(range(0, len(buildings)))
    print(selected_rows)
    data_to_return = buildings.to_dict("records")
    return columns, row_selectable, selected_rows, hidden_columns, data_to_return


@app.callback(
    [
        Output("osfi-dates-rangeslider", "min"),
        Output("osfi-dates-rangeslider", "max"),
        Output("osfi-dates-rangeslider", "marks"),
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
    return min_value, max_value, marks


@app.callback(
    Output("osfi-dates-rangeslider", "value"),
    [
        Input("osfi-dates-rangeslider-min-down", "n_clicks"),
        Input("osfi-dates-rangeslider-min-up", "n_clicks"),
        Input("osfi-dates-rangeslider-max-down", "n_clicks"),
        Input("osfi-dates-rangeslider-max-up", "n_clicks"),
        Input("osfi-dates-rangeslider", "marks"),
    ],
    [State("osfi-dates-rangeslider", "value"),],
)
def update_sliders_values(
    min_down_n_clicks, min_up_n_clicks, max_down_clicks, max_up_clicks, rangeslider_marks, rangeslider_values
):
    ctx = dash.callback_context
    # If values of the range slider are not set, we take the first and last mark
    if rangeslider_values is None:
        marks = list(rangeslider_marks)
        return [int(marks[0]), int(marks[-1])]

    if not ctx.triggered:
        raise PreventUpdate
    else:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        marks = [int(m) for m in rangeslider_marks]
        min_value = rangeslider_values[0]
        min_index = marks.index(min_value)
        max_value = rangeslider_values[1]
        max_index = marks.index(max_value)
        if prop_id == "osfi-dates-rangeslider-min-down":
            if min_index > 0:
                min_value = marks[min_index - 1]
        elif prop_id == "osfi-dates-rangeslider-min-up":
            if min_index < len(marks):
                min_value = marks[min_index + 1]
        elif prop_id == "osfi-dates-rangeslider-max-down":
            if max_index > 0:
                max_value = marks[max_index - 1]
        elif prop_id == "osfi-dates-rangeslider-max-up":
            if max_index < len(marks):
                max_value = marks[max_index + 1]
        return [int(min_value), int(max_value)]


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
    Output("osfi-building-location", "figure"),
    [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_map_location(selected_rows, slider_values, selected_entity, buildings):
    # Here we select all the data
    data_to_display = get_data(selected_entity, list(range(len(buildings))), buildings, slider_values)
    return get_building_location(buildings, data_to_display, selected_rows)


@app.callback(
    Output("osfi-repartition-consumption-pies", "figure"),
    [
        Input("dashboard-selected-entity", "children"),
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-all-data-table", "data"),
        Input("osfi-dates-rangeslider", "value"),
    ],
)
def update_repartition_consumption_pies(selected_entity, selected_rows, buildings, slider_values):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    consumption_pies = get_repartition_consumption_pies(data_to_display)
    return consumption_pies


@app.callback(
    Output("osfi-repartition-emission-pies", "figure"),
    [
        Input("dashboard-selected-entity", "children"),
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-all-data-table", "data"),
        Input("osfi-dates-rangeslider", "value"),
    ],
)
def update_repartition_emission_pies(selected_entity, selected_rows, buildings, slider_values):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    emission_pies = get_repartition_emission_pies(data_to_display)
    return emission_pies


#
#
# @app.callback(
#     Output("emission-gas-pie", "figure"),
#     [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
#     [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
# )
# def update_gas_pie(selected_rows, slider_values, selected_entity, buildings):
#     data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
#     gas_pie_graph = get_pie(data_to_display, "emission_gaz")
#     return gas_pie_graph


@app.callback(
    Output("osfi-consumption-timeseries-per-building", "figure"),
    [
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-dates-rangeslider", "value"),
        Input("osfi-display-mode-dropdown", "value"),
    ],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_consumption_timeseries_per_building(selected_rows, slider_values, display_mode, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    consumption_time_series = get_consumption_timeseries_per_building(data_to_display, display_mode)
    return consumption_time_series


# @app.callback(
#     Output("osfi-emission-timeseries-per-building", "figure"),
#     [
#         Input("osfi-all-data-table", "selected_rows"),
#         Input("osfi-dates-rangeslider", "value"),
#         Input("osfi-display-mode-dropdown", "value"),
#     ],
#     [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
# )
# def update_emission_timeseries_per_building(selected_rows, slider_values, display_mode, selected_entity, buildings):
#     data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
#     emission_time_series = get_emission_timeseries_per_building(data_to_display, display_mode)
#     return emission_time_series


@app.callback(
    Output("osfi-consumption-timeseries", "figure"),
    [
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-dates-rangeslider", "value"),
        Input("osfi-display-mode-dropdown", "value"),
    ],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_consumption_timeseries(selected_rows, slider_values, display_mode, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    consumption_time_series = get_consumption_timeseries(data_to_display, display_mode)
    return consumption_time_series


@app.callback(
    Output("osfi-emission-timeseries", "figure"),
    [
        Input("osfi-all-data-table", "selected_rows"),
        Input("osfi-dates-rangeslider", "value"),
        Input("osfi-display-mode-dropdown", "value"),
    ],
    [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
)
def update_emission_timeseries(selected_rows, slider_values, display_mode, selected_entity, buildings):
    data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
    emission_time_series = get_emission_timeseries(data_to_display, display_mode)
    return emission_time_series


# @app.callback(
#     Output("gas_time_series", "figure"),
#     [Input("osfi-all-data-table", "selected_rows"), Input("osfi-dates-rangeslider", "value")],
#     [State("dashboard-selected-entity", "children"), State("osfi-all-data-table", "data")],
# )
# def update_gas_time_series(selected_rows, slider_values, selected_entity, buildings):
#     data_to_display = get_data(selected_entity, selected_rows, buildings, slider_values)
#     gas_time_series = get_emissions_timeseries(data_to_display, "emission_gaz")
#
#     return gas_time_series
