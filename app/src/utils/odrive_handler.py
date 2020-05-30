import pandas as pd


class OdriveHandler:
    """"
        Class for loading Odrive data and returning
    """

    def __init__(self):
        self.data = pd.read_csv("/data/cleaned/data_odrive.csv")

    def get_structure_data(self, code_structure=None, filter_motorisation=None):
        if filter_motorisation is not None:
            return self.data.loc[self.data["Motorisation"] == code_structure].loc[
                self.data["Entité 2"] == code_structure, :
            ]
        if code_structure is not None:
            return self.data.loc[self.data["Entité 2"] == code_structure, :]
        return self.data


ov = OdriveHandler()
