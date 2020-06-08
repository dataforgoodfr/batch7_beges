import numpy as np
import pandas as pd

CHORUS_DT_DATA_PATH = "/data/cleaned/data_chorus_dt.csv"


class ChorusDtHandler:
    """"
        Class for loading chorus DT data and returning
    """

    def __init__(self):
        self.data_path = CHORUS_DT_DATA_PATH
        self.prestation_dict = {"A": "Avion", "T": "Train", "TC": "Transport en commun"}
        self.data = self.load_data()
        self.preprocess_data()
        self.prestation_options = self.get_prestation_options()
        self.year_options = self.get_year_options()

    def load_data(self):
        col_types = {"distance": np.float64, "CO2e/trip": np.float64}
        df = pd.read_csv(self.data_path, dtype=col_types)

        return df

    def preprocess_data(self):
        self.data["count"] = 1
        self.data["prestation"] = self.data["prestation"].replace(self.prestation_dict)
        self.data["date_debut_mission"] = pd.to_datetime(self.data["date_debut_mission"])
        self.data["date_fin_mission"] = pd.to_datetime(self.data["date_fin_mission"])
        self.data.loc[:, "year_month"] = self.data["date_debut_mission"].dt.to_period("M")
        self.data["distance_group"] = pd.cut(
            self.data["distance"],
            bins=[0, 100, 500, 1000, float("inf")],
            labels=["0-100", "100-500", "500-1000", ">1000"],
        )
        self.data["lieu1"] = (
            self.data["lieu_depart"].str.extract("\ - (.*)")[0].str.replace("[\(\[].*?[\)\]]", "").str[:24]
        )
        self.data["lieu2"] = (
            self.data["lieu_arrivee"].str.extract("\ - (.*)")[0].str.replace("[\(\[].*?[\)\]]", "").str[:24]
        )
        loc1_st_loc2 = self.data["lieu1"] <= self.data["lieu2"]
        self.data.loc[loc1_st_loc2, "trajet"] = (
            self.data.loc[loc1_st_loc2, "lieu1"] + " <-> " + self.data.loc[loc1_st_loc2, "lieu2"]
        )
        self.data.loc[~loc1_st_loc2, "trajet"] = (
            self.data.loc[~loc1_st_loc2, "lieu2"] + " <-> " + self.data.loc[~loc1_st_loc2, "lieu1"]
        )
        pass

    def get_structure_data(self, code_structure=None):
        """"
            Returns pandas dataframe with Chorus DT data filtered on a code_structure.
        """
        if code_structure is not None:
            return self.data.loc[self.data.code_structure == code_structure, :]
        return self.data

    def get_prestation_options(self):
        unique_prestations = self.data.loc[:, "prestation"].unique()
        return [{"label": prestation, "value": prestation} for prestation in unique_prestations]

    def get_year_options(self):
        years = self.data["date_debut_mission"].dt.year.unique()
        return [{"label": year, "value": year} for year in years]


ch = ChorusDtHandler()


if __name__ == "__main__":
    print(ch.data["distance_group"].value_counts())
