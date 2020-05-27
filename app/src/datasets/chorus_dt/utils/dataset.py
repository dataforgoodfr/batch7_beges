import glob
import pandas as pd

COLUMNS_MAPPING = {
    "N° de l'OM": "num_om",
    "Mode de réservation (online, offline)": "mode_reservation",
    "Structure": "structure",
    "Date de début mission": "date_debut_mission",
    "Date de fin mission": "date_fin_mission",
    "Statut": "status",
    "Lieu de départ": "lieu_depart",
    "Lieu d'arrivée": "lieu_arrivee",
    "Type de prestation": "prestation_type",
    "Lieu étape": "lieu_etape",
    "Nombre de prestations": "nombre_prestation",
    "Nombre d'OM": "nombre_om",
    "Nombre de jours": "nombre_jours",
    "Coût des prestations": "cout",
}
REVERSE_COLUMNS_MAPPING = {v: k for k, v in COLUMNS_MAPPING.items()}


def get_data(dir_path, prestation_types=None):
    data = load_data(dir_path)
    data = clean_data(data, prestation_types)
    return data


def load_data(dir_path):
    datas = []
    for filepath in glob.glob(dir_path + "/Reportings_*.csv"):
        dataset = pd.read_csv(filepath, delimiter=";")
        datas.append(dataset)
    data = pd.concat(datas, ignore_index=True)
    return data


def clean_data(data, prestation_types=None):
    data.rename(columns=COLUMNS_MAPPING, inplace=True)
    data = data[data["status"] == "T - Traité"]
    data["code_structure"] = data["structure"].apply(split_code_structure)
    # Keeping only the T / TU / TC... codes
    data["prestation_type_code"] = data["prestation_type"].apply(lambda x: x.split(" - ")[0])
    if prestation_types is not None:
        data = data[data["prestation_type_code"].isin(prestation_types)]
        print("Prestation types: ")
        print(data["prestation_type"].unique())
    return data


def split_code_structure(x):
    codes = x.split(" - ")
    code_0 = codes[0]
    if "-" in code_0:
        code_0 = code_0.split("-")[0]
    return code_0


def get_places(data):

    current_data = data.copy()

    lieu_depart_count = current_data["lieu_depart"].value_counts().to_frame().reset_index()
    lieu_depart_count.columns = ["place", "src"]
    lieu_arrivee_count = current_data["lieu_arrivee"].value_counts().to_frame().reset_index()
    lieu_arrivee_count.columns = ["place", "dst"]

    lieu_etape_count = current_data["lieu_etape"].value_counts().to_frame().reset_index()
    lieu_etape_count.columns = ["place", "stop"]

    places = pd.merge(lieu_depart_count, lieu_arrivee_count, how="outer", on="place")
    places = pd.merge(places, lieu_etape_count, how="outer", on="place")
    places.fillna(0, inplace=True)
    places["total"] = places["src"] + places["dst"] + places["stop"]

    return places
