import os
import pandas as pd


def main():
    data_xls = pd.read_excel("/data/raw/odrive.xlsx.", index_col=None)
    data_xls.to_csv("/data/cleaned/odrive.csv", encoding="utf-8")


if __name__ == "__main__":
    main()
