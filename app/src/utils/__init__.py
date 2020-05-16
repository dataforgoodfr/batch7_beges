import numpy as np
import pandas as pd
import io

if __name__ == "__main__":
    import os, sys, inspect

    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

from utils.organization_chart import oc
from utils.chorus_dt_handler import ch
from utils.odrive_handler import ov
from utils.osfi_handler import oh


class DataExport:
    def __init__(self, selected_entity):
        self.service = oc.get_entity_by_id(selected_entity)
        self.load_data()

    def load_data(self):
        self.chorus_dt_df = ch.get_structure_data(self.service.code_chorus).copy()
        self.odrive_df = ov.get_structure_data(self.service.code_odrive).copy()
        self.osfi_df = oh.get_structure_data(self.service.code_osfi).copy()
        pass

    def get_file_as_bytes(self):
        """Function returns Excel data as bytes array. It avoids the need to create a file in memory.
            See https://xlsxwriter.readthedocs.io/working_with_pandas.html#additional-pandas-and-excel-information"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            self.chorus_dt_df.to_excel(writer, sheet_name="data_chorus_dt")
            self.odrive_df.to_excel(writer, sheet_name="data_odrive")
            self.osfi_df.to_excel(writer, sheet_name="data_osfi")
        writer.save()
        xlsx_data = output.getvalue()


if __name__ == "__main__":
    print("OK")
