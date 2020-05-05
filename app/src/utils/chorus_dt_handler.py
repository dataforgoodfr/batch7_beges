import pandas as pd


class ChorusDtHandler:
    """"
        Class for loading chorus DT data and returning
    """

    def __init__(self):
        self.data = pd.read_csv('/data/trips_with_month.csv')
        self.add_columns()

    def add_columns(self):
        self.data['cumulative_distance'] = self.data['count']*self.data['distance']

    def get_structure_data(self, code_structure=None):
        """"
            Returns pandas dataframe with Chorus DT data filtered on a code_structure.
        """

        if code_structure is not None:
            return self.data.loc[self.data.code_structure == code_structure, :]
        return self.data


ch = ChorusDtHandler()
