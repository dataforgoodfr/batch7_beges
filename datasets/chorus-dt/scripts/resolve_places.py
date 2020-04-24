import os
from math import radians, cos, sin, asin, sqrt
import sys
import time

import requests
import dill
import urllib.parse
import pandas as pd
import pandas.api.types as ptypes
from tqdm import tqdm
from utils.config import CONFIG

from utils import dataset
from utils.resolvers import HardcodesResolver, GeocodingApiResolver

tqdm.pandas()


def compute_distance(df:pandas.DataFrame):

    """
    
    Takes as input lat/lon positions of travel steps. Expects two 
    columns, each composed of str that encompasses the lat/long coordinates.

    Returns pandas Series of distances in km.

    """

    assert len(df.columns) == 2
    assert all(ptypes.is_string_dtype(df[col]) for col in df.columns)

    first_coord = df.iloc[:, 0]
    second_coord = df.iloc[:, 1]
    
    lon0 = first_coord.str.split(';', expand = True).iloc[:, 0].astype(float)
    lat0 = first_coord.str.split(';', expand = True).iloc[:, 1].astype(float)
    lon1 = second_coord.str.split(';', expand = True).iloc[:, 0].astype(float)
    lat1 = second_coord.str.split(';', expand = True).iloc[:, 1].astype(float)
        
    lon0 = np.deg2rad(lon0)
    lon1 = np.deg2rad(lon1)
    lat0 = np.deg2rad(lat0)
    lat1 = np.deg2rad(lat1)

    # haversine formula
    dlon = lon1 - lon0
    dlat = lat1 - lat0
    a = np.sin((dlat)/2) ** 2 + np.cos(lat1) * np.cos(lat0) * np.sin((dlon)/ 2)** 2
    
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in miles. Use 6371 for kilometers
    
    return c*r


if __name__ == "__main__":
    data = dataset.load_data("./data/raw/sample-avion-train.csv")
    places, trips = dataset.get_places_and_trips(data, ["T"])

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

    # when analyzing plane trips, doesn't work if
    # 'no stop' in trips columns. (ie. always since we programed
    # plane trips this way.)

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

    trips["distance_1"] = trips[['place_0_coords', 'place_1_coords']].apply(compute_distance, axis=1)
        trips["distance_2"] = trips[['place_1_coords', 'place_2_coords']].apply(compute_distance, axis=1)
    trips["distance_2"] = compute_distance(trips, 2)
    trips["distance"] = trips["distance_1"] + trips["distance_2"]

    places.to_csv("./data/clean/places.csv", index=False)
    trips.to_csv("./data/clean/trips.csv", index=False)
