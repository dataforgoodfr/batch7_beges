from pathlib import Path
import pandas as pd

ELECTRICITY_EMISSION_FACTOR = 0.0571  # kgCO2e/kWh
GAS_EMISSION_FACTOR = 0.227  # kgCO2e/kWh


def add_emission_columns(data):
    data["emission_electricity"] = ELECTRICITY_EMISSION_FACTOR * data["Consommation d'électricité (kWh)"]
    data["emission_gaz"] = GAS_EMISSION_FACTOR * data["Consommation de gaz (kWh)"]
    return data


def load_data(monthly_data_path, buildings_data_path):
    monthly_data = pd.read_csv(monthly_data_path, delimiter=";")
    buildings = pd.read_csv(buildings_data_path, delimiter=";")
    columns_not_in_monthly = list(buildings.columns.difference(monthly_data.columns)) + ["Code bien"]
    data = monthly_data.merge(buildings[columns_not_in_monthly], how="left", left_on="Code bien", right_on="Code bien")
    return data


def main():
    raw_data_path = Path("/data/raw/osfi")
    monthly_data_path = raw_data_path / "osfi_monthly.csv"
    buildings_data_path = raw_data_path / "osfi_buildings.csv"
    data = load_data(monthly_data_path, buildings_data_path)
    data = add_emission_columns(data)
    data.to_csv("/data/cleaned/data_osfi.csv", index=False)


if __name__ == "__main__":
    main()
