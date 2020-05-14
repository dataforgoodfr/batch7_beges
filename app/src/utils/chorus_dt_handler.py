import numpy as np
import pandas as pd

CHORUS_DT_DATA_PATH = "/data/cleaned/data_chorus_dt.csv"


class ChorusDtHandler:
    """"
        Class for loading chorus DT data and returning
    """

    def __init__(self):
        self.data_path = CHORUS_DT_DATA_PATH
        self.data = self.load_data()
        self.preprocess_data()

    def load_data(self):
        col_types = {"distance": np.float64, "CO2e/trip": np.float64}
        df = pd.read_csv(self.data_path, dtype=col_types)

        return df

    def preprocess_data(self):
        self.data["date_debut_mission"] = pd.to_datetime(self.data["date_debut_mission"])
        self.data["date_fin_mission"] = pd.to_datetime(self.data["date_fin_mission"])
        self.data.loc[:, "year_month"] = self.data["date_debut_mission"].dt.to_period("M")

    def get_structure_data(self, code_structure=None):
        """"
            Returns pandas dataframe with Chorus DT data filtered on a code_structure.
        """

        if code_structure is not None:
            return self.data.loc[self.data.code_structure == code_structure, :]
        return self.data


ch = ChorusDtHandler()
