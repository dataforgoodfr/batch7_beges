import pandas as pd


class OsfiHandler:
    def __init__(self):
        self.data = pd.read_csv("/data/cleaned/data_osfi.csv")

    def get_structure_data(self, code_structure, year=2020):
        return self.data.loc[(self.data.id == code_structure) & (self.data["Année"] == year), :]


oh = OsfiHandler()
