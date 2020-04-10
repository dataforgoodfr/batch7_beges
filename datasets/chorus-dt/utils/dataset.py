import pandas as pd


def load_data(data_path):
    columns_mapping = {
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
    data = pd.read_csv(data_path, delimiter="\t")
    data.rename(columns=columns_mapping, inplace=True)
    return data[data["status"] == "T - Traité"]


def get_places_and_trips(data, prestation_types=None):
    current_data = data.copy()
    if prestation_types is None:
        prestation_types = ["A", "AM", "AU", "T", "TC", "TCA", "TM", "TU"]

    prestation_type_filters = ["^" + d + " -" for d in prestation_types]
    current_data = current_data[
        current_data["prestation_type"].str.contains("|".join(prestation_type_filters))
    ]
    # Keeping only the T / TU / TC... codes
    current_data["prestation_type"] = current_data["prestation_type"].apply(
        lambda x: x.split(" - ")[0]
    )

    print("Prestation types: ")
    print(current_data["prestation_type"].unique())

    lieu_depart_count = (
        current_data["lieu_depart"].value_counts().to_frame().reset_index()
    )
    lieu_depart_count.columns = ["place", "src"]
    lieu_arrivee_count = (
        current_data["lieu_arrivee"].value_counts().to_frame().reset_index()
    )
    lieu_arrivee_count.columns = ["place", "dst"]
    lieu_etape_count = (
        current_data["lieu_etape"].value_counts().to_frame().reset_index()
    )
    lieu_etape_count.columns = ["place", "stop"]
    print(len(lieu_arrivee_count))
    print(len(lieu_depart_count))
    places = pd.merge(lieu_depart_count, lieu_arrivee_count, how="outer", on="place")
    places = pd.merge(places, lieu_etape_count, how="outer", on="place")
    places.fillna(0, inplace=True)
    places["total"] = places["src"] + places["dst"] + places["stop"]

    all_trips = pd.DataFrame()
    places_columns = ["lieu_depart", "lieu_etape", "lieu_arrivee"]
    all_trips["trip_slug"] = current_data[places_columns].apply(
        lambda x: " <-> ".join(x), axis=1
    )
    all_trips["trip_place_0"] = current_data["lieu_depart"]
    all_trips["trip_place_1"] = current_data["lieu_etape"]
    all_trips["trip_place_2"] = current_data["lieu_arrivee"]
    all_trips["prestation_type"] = current_data["prestation_type"]
    trips = (
        all_trips.reset_index()
        .groupby(
            [
                "trip_slug",
                "prestation_type",
                "trip_place_0",
                "trip_place_1",
                "trip_place_2",
            ],
            as_index=False,
        )
        .count()
    )
    trips.columns = [
        "trip_slug",
        "prestation_type",
        "trip_place_0",
        "trip_place_1",
        "trip_place_2",
        "count",
    ]
    trips.sort_values(by="count", inplace=True, axis=0, ascending=False)

    print("Unique places src: ", len(current_data["lieu_depart"].unique()))
    print("Unique places dst: ", len(current_data["lieu_arrivee"].unique()))
    print("Unique places stop: ", len(current_data["lieu_etape"].unique()))
    print("Unique places: ", places.shape[0])
    print("Unique trips: ", len(all_trips["trip_slug"].unique()))
    return places, trips
