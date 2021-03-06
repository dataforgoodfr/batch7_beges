import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Output, Input, State
import numpy as np

from app import app
from utils.organization_chart import OrganizationChart
from utils.chorus_dt_handler import ch
from components.html_components import build_figure_container, build_card_indicateur
from components.figures_templates import xaxis_format


def get_kpi_emissions(df):
    return "{:,}".format(int(np.round(df["CO2e/trip"].sum(), 0))).replace(",", " ")


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
    prestation_df["CO2e/trip"] = np.round(prestation_df["CO2e/trip"], 0)
    prestation_df = prestation_df.rename(columns={"prestation": "Prestation", "CO2e/trip": "Total eqCO2 (kg)",})
    fig = px.pie(
        prestation_df, values="Total eqCO2 (kg)", names="Prestation", color="Prestation", hole=0.3, opacity=0.8
    )
    fig.update_layout(
        plot_bgcolor="white",
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},
        legend_orientation="h",
        xaxis=xaxis_format,
    )
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
        plot_bgcolor="white",
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},
        xaxis=xaxis_format,
        yaxis={"title": "Émissions (kg eqCO2)"},
    )
    return fig


def get_hist_top_emission(df):
    """
    Render and update a histogram showing top routes with most emissions.
    """
    n = 10  # Max number of top trips to show
    hist_df = (
        df.groupby(["trajet"], as_index=False)[["CO2e/trip", "count"]].sum().sort_values("CO2e/trip", ascending=False)
    )
    hist_df["cumul_emission"] = hist_df["CO2e/trip"].cumsum()
    hist_df["cumul_emission%"] = 100 * hist_df["cumul_emission"] / hist_df["CO2e/trip"].sum()
    top_hist_df = hist_df.head(n)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=top_hist_df["trajet"], y=top_hist_df["CO2e/trip"], name="Émissions")
    )  # marker_color="#373a3c"
    fig.add_trace(
        go.Scatter(
            x=top_hist_df["trajet"],
            y=top_hist_df["cumul_emission%"],
            name="Cumul (%)",
            yaxis="y2",
            marker={"color": "orange"},
        )
    )
    fig.update_layout(
        plot_bgcolor="white",
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},
        xaxis=xaxis_format,
        yaxis={"title": "Émissions (kg eqCO2)"},
        yaxis2={
            "side": "right",
            "range": [0, 100],
            "title": "Part cumulative des émissions",
            "tickfont": {"color": "orange"},
            "titlefont": {"color": "orange"},
            "overlaying": "y",
            "ticksuffix": "%",
        },
    )
    fig.update_xaxes(tickfont=dict(size=10))
    return fig


def get_dashtable_by_emission(df):
    """
    Render a dashtable listing top offending connexions by CO2 emissions
    """
    # TODO: Follow instructions in https://stackoverflow.com/questions/58804477/plotly-dash-table-callback
    distance_df = df.groupby(["trajet", "prestation", "distance"])[["CO2e/trip", "count"]].sum().reset_index()
    distance_df["avg_CO2e"] = distance_df["CO2e/trip"] / distance_df["count"]
    distance_df["distance"] = distance_df["distance"].round(0)
    distance_df[["CO2e/trip", "avg_CO2e"]] = distance_df[["CO2e/trip", "avg_CO2e"]].round(2)
    distance_df = distance_df.sort_values(["CO2e/trip"], ascending=False)
    distance_df = distance_df.rename(
        columns={
            "trajet": "Trajet",
            "prestation": "Prestation",
            "distance": "Distance (km)",
            "CO2e/trip": "Total eqCO2 (kg)",
            "count": "Nombre",
        }
    )
    table = dash_table.DataTable(
        id="datatable-row-ids",
        columns=[
            {"name": i, "id": i, "deletable": True}
            for i in distance_df.columns
            # omit the id column
            if i != "id"
        ],
        data=distance_df.to_dict("rows"),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=15,
    )
    return table


def get_scatter_by_emission(df):
    """
        Render and update a bubble chart figure to show emissions distribution by prestation type/distance
    """
    distance_df = df.groupby(["prestation", "trajet", "distance"])[["CO2e/trip", "count"]].sum().reset_index()
    distance_df["avg_CO2e"] = distance_df["CO2e/trip"] / distance_df["count"]
    distance_df = distance_df.rename(
        columns={
            "trajet": "Trajet",
            "prestation": "Prestation",
            "distance": "Distance (km)",
            "CO2e/trip": "Total eqCO2 (kg)",
            "count": "Nombre",
        }
    )
    xaxis_format_updated = xaxis_format
    xaxis_format_updated["title"] = "Distance (km) - Log"
    fig = px.scatter(
        distance_df,
        x="Distance (km)",
        y="Total eqCO2 (kg)",
        size="Nombre",
        color="Prestation",
        hover_name="Trajet",
        log_x=True,
        log_y=True,
        size_max=60,
    )
    fig.update_layout(
        plot_bgcolor="white",
        template="plotly_white",
        margin={"t": 30, "r": 30, "l": 30},
        xaxis=xaxis_format_updated,
        yaxis={"title": "Émissions (kg eCO2) - Log"},
    )
    return fig


select_prestation_type = dbc.Checklist(
    id="select-prestation_type",
    options=ch.prestation_options,
    value=[p["value"] for p in ch.prestation_options],
    inline=True,
)

select_travel_year = dbc.Checklist(
    options=ch.year_options, value=[p["value"] for p in ch.year_options], id="select-travel-year", inline=True,
)

select_unreliable = dbc.Checklist(
    options=[{"label": "Inclure les trajets peu fiables", "value": False},],
    value=[True],
    id="select-unreliable",
    switch=True,
)


cards = dbc.CardDeck(
    [
        build_card_indicateur("Émissions (kg eqCO2)", "0", "kpi-emissions"),
        build_card_indicateur("Nombre de trajets", "0", "kpi-trips"),
        build_card_indicateur("Distance totale (km)", "0", "kpi-distance"),
    ]
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Jumbotron(
                            [
                                html.P(
                                    "Les émissions des trajets sont obtenues en croisant le facteur d'émission du "
                                    "type de trajet (e.g. train, avion) avec la distance parcourue. Des biais de calcul"
                                    "subsistent. Cliquer ci-dessous pour en savoir plus sur les hypothèses de calcul."
                                ),
                                dbc.Button(
                                    "En savoir plus",
                                    color="primary",
                                    href="/methodologie#methodologie_chorus",
                                    external_link=True,
                                    target="_blank",
                                ),
                            ]
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Filtres"),
                                    html.Br(),
                                    dbc.FormGroup([dbc.Label("Type de prestation"), select_prestation_type]),
                                    dbc.FormGroup([dbc.Label("Années d'étude"), select_travel_year]),
                                    dbc.FormGroup([dbc.Label("Fiabilité déplacement"), select_unreliable]),
                                    html.Br(),
                                    dbc.Button(
                                        "Appliquer", color="primary", className="mr-1", id="button-apply-filters"
                                    ),
                                ]
                            ),
                            className="pretty_container",
                        ),
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
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        build_figure_container(
                                            title="Évolution temporelles des émissions", id="timeseries-chorus-dt",
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
                            title="Pareto des liaisons avec les plus gros volumes d'émissions",
                            id="hist-by-emission",
                            footer="Dix plus gros trajets émetteurs d'émissions. "
                            "Voir le tableau pour plus de détails sur les trajets.",
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H4("Liste des trajets classés par contribution aux émissions totales"),
                        html.Div(
                            id="table-by-emission",
                            className="m-2",
                            style={"overflow-x": "scroll", "padding-right": "10px", "padding-left": "15px"},
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        build_figure_container(
                            title="Répartition des liaisons par émissions, distance et volume",
                            id="scatter-by-emission",
                            footer="Chaque liaison est représentée par une bulle dont la grosseur dépend du nombre de "
                            "trajets. Les axes des abscisses et ordonnées sont à l'échelle logarithmique.",
                        )
                    ],
                    width=12,
                ),
            ]
        ),
    ],
    id="div-data-chorus-dt",
)


@app.callback(
    [
        Output("kpi-emissions", "children"),
        Output("kpi-trips", "children"),
        Output("kpi-distance", "children"),
        Output("donut-by-prestation", "figure"),
        Output("scatter-by-emission", "figure"),
        Output("timeseries-chorus-dt", "figure"),
        Output("hist-by-emission", "figure"),
        Output("table-by-emission", "children"),
    ],
    [Input("dashboard-selected-entity", "children"), Input("button-apply-filters", "n_clicks")],
    state=[
        State("select-prestation_type", "value"),
        State("select-travel-year", "value"),
        State("select-unreliable", "value"),
    ],
)
def update_graphs(selected_entity, n_clicks, prestation_types: list, years, unreliable):
    oc = OrganizationChart()
    oc.load_current()
    service = oc.get_entity_by_id(selected_entity)
    chorus_dt_df = ch.get_structure_data(service.code_chorus).copy()
    if "fiable" not in chorus_dt_df.columns:
        chorus_dt_df["fiable"] = True
    filters = (
        chorus_dt_df.prestation.isin(prestation_types)
        & chorus_dt_df.date_debut_mission.dt.year.isin(years)
        & (chorus_dt_df.fiable.isin(unreliable) | chorus_dt_df.fiable)
    )
    chorus_dt_df = chorus_dt_df.loc[filters, :]
    return [
        get_kpi_emissions(chorus_dt_df),
        get_kpi_trips_count(chorus_dt_df),
        get_kpi_distance(chorus_dt_df),
        get_donut_by_prestation_type(chorus_dt_df),
        get_scatter_by_emission(chorus_dt_df),
        get_emissions_timeseries(chorus_dt_df),
        get_hist_top_emission(chorus_dt_df),
        get_dashtable_by_emission(chorus_dt_df),
    ]
