import requests
import urllib.parse
import os
from tqdm import tqdm
import dill
import dataset

tqdm.pandas()


class Resolver():

    def __init__(self):

        self.p_cache = 'cache.pkl'
        self._cache = self.load_cache()

    def resolve(self, search):
        token = "35872910-ffb5-4351-a874-708076572167"
        search = urllib.parse.quote(search)
        if search not in self._cache:
            print('Resolving: ', search)
            try:
                r = requests.get("https://api.navitia.io/v1/places?q=%s" % search,
                        headers={"Authorization": token})
                self._cache[search] = r.json()
            except Exception as e:
                print(e)
                self._cache[search] = None
            self.save_cache()
        return self._cache[search]


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




if __name__ == "__main__":
    data = dataset.load_data('./data/avion-train.csv')
    places, trips = dataset.get_places_and_trips(data, 'T')
    result = places['place'].str.extract("([^-]*)\s-\s([^\[]*)\s?([\[](.*)[\]])?", expand=True)
    result.drop(columns=[2], inplace=True)
    result.columns = ['code_1', 'name', 'code_2']

    resolver = Resolver()

    result['resolution'] = result['name'].progress_apply(lambda x: resolver.resolve(x))
