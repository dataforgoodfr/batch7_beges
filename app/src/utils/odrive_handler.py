import pandas as pd


class OdriveHandler:
    """"
        Class for loading Odrive data and returning
    """

    def __init__(self):
        self.data = pd.read_csv("/data/cleaned/data_odrive.csv")

    def get_structure_data(self, code_structure=None, filter_motorisation=None, filter_emissions=None):
        temp = self.data
        if filter_motorisation is not None:
            temp = temp.loc[temp["Motorisation"] == code_structure]
        if code_structure is not None:
            temp = temp.loc[temp["Entité 2"] == code_structure, :]
        if filter_emissions is not None:
            temp = temp.loc[filter_emissions[1] >= temp["CO2 (g/km)"] >= filter_emissions[0], :]
        return temp


ov = OdriveHandler()
