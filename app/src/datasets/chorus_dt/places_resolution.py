import os
from math import radians, cos, sin, asin, sqrt
import sys
import time

import requests
import dill
import numpy as np
import urllib.parse
import pandas as pd
from tqdm import tqdm

from .utils import dataset
from .utils.resolvers import HardcodesResolver, GeocodingApiResolver
from .utils.carbon_emission_counter import carbon_count

GMAP_API_KEY = os.getenv("GMAP_API_KEY")
tqdm.pandas()


def compute_distances(data):
    data["distance_0"] = np.NaN
    data["distance_1"] = np.NaN
    data["distance_2"] = np.NaN

    pairs = [("lieu_depart", "lieu_etape"), ("lieu_etape", "lieu_arrivee"), ("lieu_depart", "lieu_arrivee")]

    for distance_i, (column_0, column_1) in enumerate(pairs):
        data["distance_%s" % distance_i] = compute_distance_between_points(
            data["%s_lon" % column_0], data["%s_lat" % column_0], data["%s_lon" % column_1], data["%s_lat" % column_1]
        )
    data["distance_0"].fillna(0, inplace=True)
    data["distance_1"].fillna(0, inplace=True)
    data["distance_2"].fillna(0, inplace=True)

    # to be modified in later chorus dt fix
    data["distance"] = data[["distance_0", "distance_1", "distance_2"]].sum(axis=1)

    return data


def compute_distance_between_points(lon0, lat0, lon1, lat1):

    lon0 = np.deg2rad(lon0)
    lon1 = np.deg2rad(lon1)
    lat0 = np.deg2rad(lat0)
    lat1 = np.deg2rad(lat1)

    # haversine formula
    dlon = lon1 - lon0
    dlat = lat1 - lat0
    a = np.sin((dlat) / 2) ** 2 + np.cos(lat1) * np.cos(lat0) * np.sin((dlon) / 2) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in miles. Use 6371 for kilometers

    return c * r


def calc_CO2(trips: pd.DataFrame, carbon: dict):

    trips.loc[
        (trips["prestation_type"] == "T - Train réservé par l'agence")
        | (trips["prestation_type"] == "TM - Train pris en charge par le ministère")
        | (trips["prestation_type"] == "TU - Train pris en charge par le missionné"),
        "prestation",
    ] = "T"

    trips.loc[
        (trips["prestation_type"] == "A - Avion réservé par l'agence")
        | (trips["prestation_type"] == "AU - Avion pris en charge par le missionn")
        | (trips["prestation_type"] == "AM - Avion pris en charge par le ministère"),
        "prestation",
    ] = "A"

    trips.loc[
        (trips["prestation_type"] == "TC - Transport en commun")
        | (trips["prestation_type"] == "TCA - Transport en commun autre qu'avion, train avec résa ou bat"),
        "prestation",
    ] = "TC"

    short_plane = (trips["prestation"] == "A") & (trips["distance"] <= 1000)
    long_plane = (trips["prestation"] == "A") & (trips["distance"] > 1000)
    train = trips["prestation"] == "T"
    commun = trips["prestation"] == "TC"

    trips.loc[short_plane, "kgCO2e/passager.km"] = carbon["CO2_short_plane"]
    trips.loc[long_plane, "kgCO2e/passager.km"] = carbon["CO2_long_plane"]
    trips.loc[train, "kgCO2e/passager.km"] = carbon["CO2_TGV"]
    trips.loc[commun, "kgCO2e/passager.km"] = carbon["CO2_TC"]

    # Planes pollute an extra 95km
    trips.loc[trips["prestation"] == "A", "distance"] += 95
    trips["CO2e/trip"] = trips["kgCO2e/passager.km"] * trips["distance"]

    return trips


def resolve_place(places):
    places = places.copy()
    # Splitting codes / name
    places[["code_1", "name", "temp", "code_2"]] = places["place"].str.extract(
        "([^-]*)\s-\s([^\[]*)\s?([\[](.*)[\]])?", expand=True
    )
    places.drop(columns=["temp"], inplace=True)

    places["resolved"] = False
    places["resolved_through_uic_code"] = False
    places["resolved_through_insee_code"] = False
    places["resolved_through_tvs_code"] = False
    places["resolved_through_iata_code"] = False
    places["resolved_through_gmap_api"] = False
    places["lon"] = None
    places["address"] = ""
    places["lat"] = None

    hardcode_resolver = HardcodesResolver()
    places = places.progress_apply(hardcode_resolver.resolve, axis=1)

    # Initiate geocoder
    geocoding_api_resolver = GeocodingApiResolver(api_name="gmap", api_key=GMAP_API_KEY)

    # Apply the geocoder with delay using the rate limiter:
    places.loc[~places["resolved"], :] = places[~places["resolved"]].progress_apply(
        geocoding_api_resolver.resolve, axis=1
    )
    geocoding_api_resolver.save_cache()
    for c in places:
        if "resolved_through_" in c:
            print(c, places[c].sum())

    places["lat"] = places["lat"].astype(float)
    places["lon"] = places["lon"].astype(float)
    places_dict = places.set_index("place").to_dict()
    return places, places_dict


def main():
    prestation_types = ["A", "AM", "AU", "T", "TC", "TCA", "TM", "TU"]
    data = dataset.get_data("/data/raw/chorus-dt", prestation_types)
    places = dataset.get_places(data)
    places, places_dict = resolve_place(places)
    carbon_dict = carbon_count()

    # when analyzing plane trips, doesn't work if
    # 'no stop' in trips columns. (ie. always since we programed
    # plane trips this way.)
    for column in ["lieu_depart", "lieu_arrivee", "lieu_etape"]:
        data["%s_resolved" % column] = data[column].apply(lambda x: places_dict["resolved"][x])
        data["%s_lat" % column] = data[column].apply(
            lambda x: places_dict["lat"][x] if places_dict["resolved"][x] else np.NaN
        )
        data["%s_lon" % column] = data[column].apply(
            lambda x: places_dict["lon"][x] if places_dict["resolved"][x] else np.NaN
        )
        data["%s_coords" % column] = data["%s_lon" % column].astype(str) + ";" + data["%s_lat" % column].astype(str)

    data = compute_distances(data)

    data = calc_CO2(data, carbon_dict)

    places.to_csv("/data/cleaned/places.csv", index=False)
    data.to_csv("/data/cleaned/data_chorus_dt.csv", index=False)


if __name__ == "__main__":
    main()
