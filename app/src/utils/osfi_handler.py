import pandas as pd


class OsfiHandler:

    column_names = {
        "emission": {
            "gas": "Emissions de CO2 par le gaz (kgCO2e)",
            "electricity": "Emissions de CO2 par l'électricité (kgCO2e)",
            "total": "Emissions de CO2 au total (kgCO2e)",
        },
        "consumption": {
            "gas": "Consommation de gaz (kWh)",
            "electricity": "Consommation d'électricité (kWh)",
            "total": "Consommation totale (kWh)",
        },
    }

    def __init__(self):
        self.data = pd.read_pickle("/data/cleaned/data_osfi.pkl")

    def get_structure_data(self, code_structure, year=None):
        if year:
            return self.data.loc[(self.data.id == code_structure) & (self.data["Année"] == year), :]
        else:
            return self.data.loc[(self.data.id == code_structure)]


oh = OsfiHandler()
