import os
from math import radians, cos, sin, asin, sqrt
import sys
import time

import requests
import dill
import urllib.parse
from geopy.geocoders import GoogleV3, Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
from tqdm import tqdm

from utils import dataset
from utils.config import config

tqdm.pandas()

def load_codes(path):
    with open(path, 'rb') as file_id:
        return dill.load(file_id)

INSEE_CODES = load_codes('./data/prepared/insee_codes.pkl')
TVS_CODES = load_codes('./data/prepared/tvs_codes.pkl')
UIC_CODES = load_codes('./data/prepared/uic_codes.pkl')
GMAP_API_KEY = config['api_keys']['gmap']


class Resolver():
    """
    Return a dataframe name / geometry / resolved name
    The cache will have the same format
    """

    def __init__(self, api_name='nominatim', api_key=None):

        if api_name == 'nominatim':
            geolocator = Nominatim(user_agent='data4good-beges')
            self.p_cache = './data/prepared/nominatim_responses.pkl'
        elif api_name == 'gmap':
            geolocator = GoogleV3(api_key=api_key, domain='maps.google.fr')
            self.p_cache = './data/prepared/gmap_responses.pkl'
        else:
            raise ValueError
        self.geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=10)
        self._cache = self.load_cache()

    def resolve(self, x):
        name = x['name']
        if name in self._cache:
            response = self._cache[name]
        else:
            response = self.geocode_with_delay(name)
            self._cache[name] = response

        if response is not None:
            x['lon'] = response.longitude
            x['lat'] = response.latitude
            x['address'] = response.address
            x['resolved'] = True
            x['resolved_through_gmap_api'] = True
        return x

    def load_cache(self):
        if os.path.isfile(self.p_cache):
            with open(self.p_cache, 'rb') as file_id:
                cache = dill.load(file_id)
        else:
            cache = {}
        return cache


    def save_cache(self):
        with open(self.p_cache, 'wb') as file_id:
            dill.dump(self._cache, file_id)

class NavitiaResolver():
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": token}
        self.base_url = "https://api.navitia.io/v1/journeys?"
        self.paramters = "from={coords_from}&to={coords_to}"

        self.p_cache = './data/prepared/navitia_response.pkl'
        self.api_key = api_key
        self._cache = self.load_cache()

    def get_journey(self, x):
        coords_from = x['coords_place_0']
        coords_to = x['coords_place_1']
        if (coords_from, coords_to) in self._cache:
            return self._cache[(coords_from, coords_to)]
        else:
            url = self.base_url + urllib.parse.quote(self.paramters.format(coords_from=coords_from, coords_to=coords_to))
            print(url)
            response = requests.get(url, headers=self.headers)
            self._cache[(coords_from, coords_to)] = response.json()

    def load_cache(self):
        if os.path.isfile(self.p_cache):
            with open(self.p_cache, 'rb') as file_id:
                cache = dill.load(file_id)
        else:
            cache = {}
        return cache


    def save_cache(self):
        with open(self.p_cache, 'wb') as file_id:
            dill.dump(self._cache, file_id)


def get_int(x):
    try:
        return int(x)
    except ValueError:
        return None


def resolve(x):
    code_2_as_int = get_int(x['code_2'])
    if code_2_as_int and (code_2_as_int in UIC_CODES['lon']):
        x['lon'] = UIC_CODES['lon'][code_2_as_int]
        x['lat'] = UIC_CODES['lat'][code_2_as_int]
        x['resolved'] = True
        x['resolved_through_uic_code'] = True
    elif x['code_1'] in INSEE_CODES['lon']:
        x['lon'] = INSEE_CODES['lon'][x['code_1']]
        x['lat'] = INSEE_CODES['lat'][x['code_1']]
        x['resolved'] = True
        x['resolved_through_insee_code'] = True
    # elif x['code_1'] in TVS_CODES['lon']:
    #     x['lon'] = TVS_CODES['lon'][x['code_1']]
    #     x['lat'] = TVS_CODES['lat'][x['code_1']]
    #     x['resolved'] = True
    #     x['resolved_through_tvs_code'] = True
    else:
        x['lon'] = None
        x['lat'] = None
    return x
    # if

def compute_distance(x):
    lon1 = x['coords_place_0_lon']
    lat1 = x['coords_place_0_lat']
    lon2 = x['coords_place_1_lon']
    lat2 = x['coords_place_1_lat']
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in miles. Use 6371 for kilometers
    return c * r


if __name__ == "__main__":
    data = dataset.load_data('./data/raw/avion-train.csv')
    places, trips = dataset.get_places_and_trips(data, 'T')

    # Splitting codes / name
    places[['code_1', 'name', 'temp', 'code_2']] = places['place'].str.extract("([^-]*)\s-\s([^\[]*)\s?([\[](.*)[\]])?", expand=True)
    places.drop(columns=['temp'], inplace=True)

    places['resolved'] = False
    places['resolved_through_uic_code'] = False
    places['resolved_through_insee_code'] = False
    places['resolved_through_tvs_code'] = False
    places['resolved_through_gmap_api'] = False
    places['lon'] = None
    places['address'] = ''
    places['lat'] = None


    places = places.progress_apply(resolve, axis=1)

    # Initiate geocoder
    # resolver = Resolver(api_name='nominatim')
    resolver = Resolver(api_name='gmap', api_key=GMAP_API_KEY)

    # Apply the geocoder with delay using the rate limiter:
    places.loc[~places['resolved'], :] = places[~places['resolved']].progress_apply(resolver.resolve, axis=1)
    resolver.save_cache()
    for c in places:
        if 'resolved_through_' in c:
            print(c, places[c].sum())

    places['lat'] = places['lat'].astype(float)
    places['lon'] = places['lon'].astype(float)
    places_dict = places.set_index('place').to_dict()

    trips['coords_place_0_lat'] = trips['trip_place_0'].apply(lambda x: places_dict['lat'][x])
    trips['coords_place_0_lon'] = trips['trip_place_0'].apply(lambda x: places_dict['lon'][x])
    trips['coords_place_1_lat'] = trips['trip_place_1'].apply(lambda x: places_dict['lat'][x])
    trips['coords_place_1_lon'] = trips['trip_place_1'].apply(lambda x: places_dict['lon'][x])
    trips['place_0_count'] = trips['trip_place_1'].apply(lambda x: places_dict['total'][x])
    trips['place_1_count'] = trips['trip_place_1'].apply(lambda x: places_dict['total'][x])
    trips['distance'] = trips.apply(compute_distance, axis=1)
    trips['coords_place_0'] = trips[ 'coords_place_0_lon'].astype(str) + ';' + trips[ 'coords_place_0_lat'].astype(str)
    trips['coords_place_1'] = trips[ 'coords_place_1_lon'].astype(str) + ';' + trips[ 'coords_place_1_lat'].astype(str)

    places.to_csv('./data/clean/places.csv', index=False)
    trips.to_csv('./data/clean/trips.csv', index=False)
