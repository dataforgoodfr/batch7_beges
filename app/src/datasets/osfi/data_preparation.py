import pandas as pd

ELECTRICITY_EMISSION_FACTOR = 0.0571  # kgCO2e/kWh
GAS_EMISSION_FACTOR = 0.227  # kgCO2e/kWh


def add_emission_columns(data):
    data["emission_electricity"] = ELECTRICITY_EMISSION_FACTOR * data["Consommation d'électricité (kWh)"]
    data["emission_gaz"] = GAS_EMISSION_FACTOR * data["Consommation de gaz (kWh)"]
    return data


def main():
    data = pd.read_csv("/data/raw/osfi/osfi.csv")
    data[["code_batiment", "code_structure"]] = data["Code bien"].str.split("_", expand=True)
    data["id"] = data["code_structure"] + ";" + data["Région"]
    data = add_emission_columns(data)
    data.to_csv("/data/cleaned/data_osfi.csv")


if __name__ == "__main__":
    main()
