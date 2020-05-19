from datasets.chorus_dt.codes_preparation import main as chorus_dt_prepare_codes
from datasets.chorus_dt.places_resolution import main as chorus_dt_resolve_places

from datasets.odrive.file_conversion import main as odrive_file_conversion
from datasets.osfi.data_preparation import main as osfi_prepare_data

if __name__ == "__main__":
    # Prepare Odrive
    print("Preparing odrive")
    odrive_file_conversion()
    # Prepare chorus dt
    print("Preparing chorus codes")
    chorus_dt_prepare_codes()
    print("Preparing chorus dataset")
    chorus_dt_resolve_places()

    # Prepare osfi
    print("Preparing osfi")
    osfi_prepare_data()
