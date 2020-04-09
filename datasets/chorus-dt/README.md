INSEE CODES : https://www.data.gouv.fr/en/datasets/base-officielle-des-codes-postaux/
LISTE DES GARES : https://ressources.data.sncf.com/explore/dataset/liste-des-gares/table

TODO:
- Get trip distance using gmap api
- Use geopy to compute distance (geopy.distance.distance)
- Tester navitia
- S'il y a un liaison TGV ou TER -> Dataset
  - TGV ou TER
      - Si TGV -> on a l'émission
      - Si Ter -> on récupère la données simple

# Usage
## Requirements
- Virtualenv
- virtualenvwrapper

## Setup
### Data
Get the following data from the drive and put them in `./data/raw`:
- datasets/chorus-dt/avion-train.csv

### Config file
```
cp config.ini.dist config.ini
```
And fill the missing values.

### Virtualenv
Setup your python environment:
```
mkvirtualenv beges --python 3.6
workon beges
pip install -r requirements.txt
```

### Datasets
Download the raw data using the `dowload_data.sh` script:
`sh scripts/download_data.sh`


## Usage
You can prepare the different datasets used for places resolution:
```
python scipts/prepare_datasets.py
```
This will create / replaces files in `data/prepared`.

You can resolve the places:
```
python scipts/resolve_places.py
```
This will create / replaces `trips.csv` and `places.csv` in `data/clean`.
