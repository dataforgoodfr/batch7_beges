import os
from math import radians, cos, sin, asin, sqrt
import sys
import time

import requests
import dill
import urllib.parse
import pandas as pd
from tqdm import tqdm
from utils.config import CONFIG

from utils import dataset
from utils.resolvers import HardcodesResolver, GeocodingApiResolver

tqdm.pandas()


def compute_distance(x):
    lon1 = x["coords_place_0_lon"]
    lat1 = x["coords_place_0_lat"]
    lon2 = x["coords_place_1_lon"]
    lat2 = x["coords_place_1_lat"]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in miles. Use 6371 for kilometers
    return c * r


if __name__ == "__main__":
    data = dataset.load_data("./data/raw/avion-train.csv")
    places, trips = dataset.get_places_and_trips(data, ["T", "TC", "TCA", "TCM", "TU"])

    # Splitting codes / name
    places[["code_1", "name", "temp", "code_2"]] = places["place"].str.extract(
        "([^-]*)\s-\s([^\[]*)\s?([\[](.*)[\]])?", expand=True
    )
    places.drop(columns=["temp"], inplace=True)

    places["resolved"] = False
    places["resolved_through_uic_code"] = False
    places["resolved_through_insee_code"] = False
    places["resolved_through_tvs_code"] = False
    places["resolved_through_gmap_api"] = False
    places["lon"] = None
    places["address"] = ""
    places["lat"] = None

    hardcode_resolver = HardcodesResolver()
    places = places.progress_apply(hardcode_resolver.resolve, axis=1)

    # Initiate geocoder
    GMAP_API_KEY = CONFIG["api_keys"]["gmap"]
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

    for place_index in [0, 1, 2]:
        trips["coords_place_%d_lat" % place_index] = trips[
            "trip_place_%d" % place_index
        ].apply(lambda x: places_dict["lat"][x])
        trips["coords_place_%d_lon" % place_index] = trips[
            "trip_place_%d" % place_index
        ].apply(lambda x: places_dict["lon"][x])
        trips["coords_place_%d" % place_index] = (
            trips["coords_place_%d_lon" % place_index].astype(str)
            + ";"
            + trips["coords_place_%d_lat" % place_index].astype(str)
        )
        trips["place_%d_count" % place_index] = trips[
            "trip_place_%d" % place_index
        ].apply(lambda x: places_dict["total"][x])

    trips["distance"] = trips.apply(compute_distance, axis=1)
    places.to_csv("./data/clean/places.csv", index=False)
    trips.to_csv("./data/clean/trips.csv", index=False)
