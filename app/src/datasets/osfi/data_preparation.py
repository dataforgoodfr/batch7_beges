from pathlib import Path
import pandas as pd

ELECTRICITY_EMISSION_FACTOR = 0.0571  # kgCO2e/kWh
GAS_EMISSION_FACTOR = 0.227  # kgCO2e/kWh


def add_emission_columns(data):
    data["Emissions de CO2 par l'électricité (kgCO2e)"] = (
        ELECTRICITY_EMISSION_FACTOR * data["Consommation d'électricité (kWh)"]
    )
    data["Emissions de CO2 par le gaz (kgCO2e)"] = GAS_EMISSION_FACTOR * data["Consommation de gaz (kWh)"]
    data["Emissions de CO2 au total (kgCO2e)"] = (
        data["Emissions de CO2 par l'électricité (kgCO2e)"] + data["Emissions de CO2 par le gaz (kgCO2e)"]
    )
    return data


def load_data(monthly_data_path, buildings_data_path):
    monthly_data = pd.read_csv(monthly_data_path, delimiter=";")
    buildings = pd.read_csv(buildings_data_path, delimiter=";")
    columns_not_in_monthly = list(buildings.columns.difference(monthly_data.columns)) + ["Code bien"]
    data = monthly_data.merge(buildings[columns_not_in_monthly], how="left", left_on="Code bien", right_on="Code bien")
    return data


def convert_string_to_float(x):
    return float(x.replace(",", "."))


def convert_string_to_float_if_string(x):
    if isinstance(x, str):
        return convert_string_to_float(x)
    else:
        return x


def clean_data(data):
    # Convert numbers in format 2,33 to float (fixing the comma issue)
    data["Consumption kwh electricity"] = (
        data["Consumption kwh electricity"].apply(convert_string_to_float_if_string).fillna(0)
    )
    data["Gas Consumption (kWh)"] = data["Gas Consumption (kWh)"].apply(convert_string_to_float_if_string).fillna(0)
    data["Consommation totale (kWh)"] = (
        data["Consommation totale (kWh)"].apply(convert_string_to_float_if_string).fillna(0)
    )
    data.rename(
        columns={
            "Consumption kwh electricity": "Consommation d'électricité (kWh)",
            "Gas Consumption (kWh)": "Consommation de gaz (kWh)",
            "longitude RT": "Longitude RT",
        },
        inplace=True,
    )
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def main():
    raw_data_path = Path("/data/raw/osfi")
    monthly_data_path = raw_data_path / "osfi_monthly.csv"
    buildings_data_path = raw_data_path / "osfi_buildings.csv"
    data = load_data(monthly_data_path, buildings_data_path)
    data = clean_data(data)
    data = add_emission_columns(data)
    data[["Code Batiment", "Code Structure"]] = data["Code bien"].str.split("_", expand=True)
    data["id"] = data["Code Structure"] + ";" + data["Région"]
    data.to_pickle("/data/cleaned/data_osfi.pkl")


if __name__ == "__main__":
    main()
