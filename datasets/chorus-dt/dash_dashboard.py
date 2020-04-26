import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np

from utils.config import config

trips = pd.read_csv("./data/clean/trips.csv")
places = pd.read_csv("./data/clean/places.csv")
trips.index.name = "id"
trips.reset_index(inplace=True)


def get_map_figure(active_row=None, active_column=None):
    center = {
        "lat": 48.85,
        "lon": 2.35,
    }
    print(center)
    state_data = [
        go.Scattermapbox(
            lat=places["lat"],
            lon=places["lon"],
            customdata=places[["name", "lat", "lon"]],
            hovertemplate="<i>%{customdata[0]}</i>"
            + "<br>Lon: %{customdata[1]}"
            + "<br>Lat: %{customdata[2]}",
            mode="markers",
            marker=dict(
                size=np.maximum(10, (places["total"] / 100)),
                color="yellow",
                opacity=0.2,
            ),
        )
    ]
    if active_row is not None:
        colors = {
            "trip_place_0": "green",
            "trip_place_1": "blue",
            "trip_place_2": "red",
        }
        opacities = {"trip_place_0": 0.5, "trip_place_1": 0.5, "trip_place_2": 0.5}
        opacities[active_column] = 0.9
        center_lat = (
            trips.loc[active_row, "coords_place_0_lat"]
            + trips.loc[active_row, "coords_place_2_lat"]
        ) / 2.0
        center_lon = (
            trips.loc[active_row, "coords_place_0_lon"]
            + trips.loc[active_row, "coords_place_2_lon"]
        ) / 2.0
        center = {
            "lat": center_lat,
            "lon": center_lon,
        }
        for place_index in [0, 1, 2]:
            state_data.append(
                go.Scattermapbox(
                    lat=[trips.loc[active_row, "coords_place_%d_lat" % place_index]],
                    lon=[trips.loc[active_row, "coords_place_%d_lon" % place_index]],
                    mode="markers",
                    customdata=trips.loc[
                        [active_row],
                        [
                            "trip_place_%d" % place_index,
                            "coords_place_%d_lon" % place_index,
                            "coords_place_%d_lat" % place_index,
                        ],
                    ],
                    hovertemplate="<i>%{customdata[0]}</i>"
                    + "<br>Lon: %{customdata[1]}"
                    + "<br>Lat: %{customdata[2]}",
                    marker=dict(
                        size=20,
                        color=colors["trip_place_%d" % place_index],
                        opacity=opacities["trip_place_%d" % place_index],
                    ),
                )
            )
    print(center)
    layout = dict(
        mapbox=dict(style="open-street-map", zoom=5, center=center,),
        # uirevision="no reset of zoom",
        margin=dict(r=0, l=0, t=0, b=0),
    )
    return {"data": state_data, "layout": layout}


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

columns_to_be_displayed = [
    "count",
    "trip_place_0",
    "trip_place_1",
    "trip_place_2",
    "prestation_type",
]
app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="seven columns",
                    children=dash_table.DataTable(
                        id="table",
                        columns=[
                            {"name": i, "id": i}
                            for i in trips.columns
                            if i in columns_to_be_displayed
                        ],
                        data=trips.to_dict("records"),
                        hidden_columns=[
                            f for f in trips.columns if f not in columns_to_be_displayed
                        ],
                        style_table={
                            "maxHeight": "500px",
                            "overflowY": "scroll",
                            "overflowX": "scroll",
                        },
                        css=[{"selector": ".show-hide", "rule": "display: none"}],
                    ),
                    style={"display": "inline-block"},
                ),
                html.Div(
                    className="five columns",
                    children=dcc.Graph(id="map"),
                    style={"display": "inline-block"},
                ),
                html.Div(id="table-container"),
            ],
        ),
    ]
)


@app.callback(
    Output("map", "figure"),
    [
        Input("table", "derived_viewport_row_ids"),
        Input("table", "selected_row_ids"),
        Input("table", "active_cell"),
    ],
)
def update_graph(row_ids, selected_row_ids, active_cell):
    if active_cell is not None:
        active_row = row_ids[active_cell["row"]]
        active_column = active_cell["column_id"]
    else:
        active_row = None
        active_column = None

    return get_map_figure(active_row, active_column)


if __name__ == "__main__":
    app.run_server(debug=True, port=config["dash"]["port"])
