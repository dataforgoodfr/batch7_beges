from datasets.chorus_dt.codes_preparation import main as chorus_dt_prepare_codes
from datasets.chorus_dt.places_resolution import main as chorus_dt_resolve_places
from datasets.osfi.data_preparation import main as osfi_prepare_data

if __name__ == "__main__":
    # Prepare chorus dt
    chorus_dt_prepare_codes()
    chorus_dt_resolve_places()

    # Prepare osfi
    osfi_prepare_data()
