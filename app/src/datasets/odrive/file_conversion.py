import pandas as pd
import math
import datetime

NAMES_TO_REPLACE = {"CLIO IV": "CLIO 4", "CLIO III": "CLIO 3", "MÉGANE": "MEGANE", "ZOÉ": "ZOE"}


def clean_modele(modele):
    modele = str(modele).upper()
    if modele in NAMES_TO_REPLACE.keys():
        modele = NAMES_TO_REPLACE.get(modele)
    return modele


def clean_date(date_value):
    if date_value == math.nan or date_value == "00/01/00" or date_value is None:
        date_value = datetime.datetime.today()
    return date_value


def main():
    data_xls = pd.read_excel("/data/raw/odrive/odrive.xlsx", index_col=None)
    data_xls["Modèle"] = data_xls["Modèle"].apply(clean_modele)
    data_xls["Date relevé"].replace(to_replace="00/01/00", value=None, inplace=True)
    data_xls["Date relevé"].fillna(datetime.datetime.today(), inplace=True)
    data_xls["Date 1ère mise en circulation"] = data_xls["Date 1ère mise en circulation"].apply(clean_date)
    data_xls["Total années cirulation"] = (data_xls["Date relevé"] - data_xls["Date 1ère mise en circulation"]).astype(
        "timedelta64[D]"
    ) / 365
    data_xls["km parcours par an"] = (
        data_xls["Dernier relevé km"].fillna(0).astype(int) / data_xls["Total années cirulation"]
    )
    data_xls["Emissions (g/an)"] = data_xls["km parcours par an"] * data_xls["CO2 (g/km)"]
    data_xls.to_csv("/data/cleaned/data_odrive.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
