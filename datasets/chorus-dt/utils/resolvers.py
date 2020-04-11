import os
import math

import dill

from geopy.geocoders import GoogleV3, Nominatim
from geopy.extra.rate_limiter import RateLimiter


class GeocodingApiResolver:
    """
    Return a dataframe name / geometry / resolved name
    The cache will have the same format
    """

    def __init__(self, api_name="nominatim", api_key=None):

        if api_name == "nominatim":
            geolocator = Nominatim(user_agent="data4good-beges")
            self.p_raw_cache = "./data/raw/nominatim_responses.pkl"
            self.p_cache = "./data/prepared/nominatim_responses.pkl"
        elif api_name == "gmap":
            geolocator = GoogleV3(api_key=api_key, domain="maps.google.fr")
            self.p_raw_cache = "./data/raw/gmap_responses.pkl"
            self.p_cache = "./data/prepared/gmap_responses.pkl"
        else:
            raise ValueError
        self.geocode_with_delay = RateLimiter(
            geolocator.geocode, min_delay_seconds=1, max_retries=10
        )
        self._cache = self.load_cache()

    def resolve(self, x):
        name = x["name"]
        if name is not None and (name != ""):
            if name in self._cache:
                response = self._cache[name]
            else:
                response = self.geocode_with_delay(name)
                self._cache[name] = response
        else:
            response = None

        if response is not None:
            x["lon"] = response.longitude
            x["lat"] = response.latitude
            x["address"] = response.address
            x["resolved"] = True
            x["resolved_through_gmap_api"] = True
        return x

    def load_cache(self):
        if os.path.isfile(self.p_cache):
            with open(self.p_cache, "rb") as file_id:
                cache = dill.load(file_id)
        else:
            with open(self.p_raw_cache, "rb") as file_id:
                cache = dill.load(file_id)
        return cache

    def save_cache(self):
        with open(self.p_cache, "wb") as file_id:
            dill.dump(self._cache, file_id)


class HardcodesResolver:
    def __init__(self):
        self.insee_codes = self.load_codes("./data/prepared/insee_codes.pkl")
        self.tvs_codes = self.load_codes("./data/prepared/tvs_codes.pkl")
        self.uic_codes = self.load_codes("./data/prepared/uic_codes.pkl")
        self.iata_codes = self.load_codes("./data/prepared/iata_codes.pkl")

    def load_codes(self, path):
        with open(path, "rb") as file_id:
            return dill.load(file_id)

    def resolve(self, x):
        code_2_as_int = self.get_int(x["code_2"])
        if code_2_as_int and (code_2_as_int in self.uic_codes["lon"]):
            x["lon"] = self.uic_codes["lon"][code_2_as_int]
            x["lat"] = self.uic_codes["lat"][code_2_as_int]
            x["resolved"] = True
            x["resolved_through_uic_code"] = True
        elif x["code_1"] in self.insee_codes["lon"]:
            x["lon"] = self.insee_codes["lon"][x["code_1"]]
            x["lat"] = self.insee_codes["lat"][x["code_1"]]
            x["resolved"] = True
            x["resolved_through_insee_code"] = True
        elif x["code_1"].str[-3:] in self.iata_codes["lon"]:
            x["lon"] = self.iata_codes["lon"][x["code_1"]]
            x["lat"] = self.iata_codes["lat"][x["code_1"]]
            x["resolved"] = True
            x["resolved_through_iata_code"] = True
        elif x["place"] == '-75056': # Hard exception...
            x["name"] = 'Paris'
        # elif x['code_1'] in TVS_CODES['lon']:
        #     x['lon'] = TVS_CODES['lon'][x['code_1']]
        #     x['lat'] = TVS_CODES['lat'][x['code_1']]
        #     x['resolved'] = True
        #     x['resolved_through_tvs_code'] = True
        else:
            x["lon"] = None
            x["lat"] = None
        return x

    def get_int(self, x):
        try:
            return int(x)
        except ValueError:
            return None
