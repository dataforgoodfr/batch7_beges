import pandas as pd


class ChorusDtHandler:
    """"
        Class for loading chorus DT data and returning
    """

    def __init__(self):
        self.data = pd.read_csv("/data/cleaned/data_chorus_dt.csv")
        self.clean_data()

    def clean_data(self):
        self.data["date_debut_mission"] = pd.to_datetime(self.data["date_debut_mission"])
        self.data["date_fin_mission"] = pd.to_datetime(self.data["date_fin_mission"])

    def get_structure_data(self, code_structure=None):
        """"
            Returns pandas dataframe with Chorus DT data filtered on a code_structure.
        """

        if code_structure is not None:
            return self.data.loc[self.data.code_structure == code_structure, :]
        return self.data


ch = ChorusDtHandler()
