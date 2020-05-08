from datasets.chorus_dt.codes_preparation import main as chorus_dt_prepare_codes
from datasets.chorus_dt.places_resolution import main as chorus_dt_resolve_places
from datasets.odrive.file_conversion import main as odrive_file_conversion

if __name__ == "__main__":
    # Prepare chorus dt
    odrive_file_conversion()
    chorus_dt_prepare_codes()
    chorus_dt_resolve_places()
