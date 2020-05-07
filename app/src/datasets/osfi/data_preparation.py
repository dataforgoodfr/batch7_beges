import pandas as pd


def main():
    data = pd.read_csv("/data/raw/osfi/osfi.csv")
    data[["code_batiment", "code_structure"]] = data["Code bien"].str.split("_", expand=True)
    data["id"] = data["code_structure"] + ";" + data["Région"]
    data.to_csv("/data/cleaned/data_osfi.csv")


if __name__ == "__main__":
    main()
