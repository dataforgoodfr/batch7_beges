# Avion train sample
curl --insecure 'https://docs.google.com/uc?export=download&id=1xD9hsfKrlh5rJoGaYqkK_PRUaFQSZmfk' -O ./data/raw/avion-train.csv
# Laposte codes
curl --insecure 'https://docs.google.com/uc?export=download&id=1EFDXoxmiXVGHwsi6aIPLXQxoMoO9y7ut' -O ./data/raw/laposte_hexasmal.csv
# Lists of train stations
curl --insecure 'https://docs.google.com/uc?export=download&id=1zLRRqbHNH4y487JKoBA-GhfPSZt-7GhF' -O ./data/raw/liste-des-gares.csv
curl --insecure 'https://docs.google.com/uc?export=download&id=1WSAj7khA-HGjTyHpWbAXzZs2JGafNkfD' -O ./data/raw/referentiel-gares-voyageurs.csv
# Gmap cache
curl --insecure 'https://docs.google.com/uc?export=download&id=1iw8q0Ve5AMusts11GrI2XzmOAbfKaclM' -O ./data/raw/gmap_responses.pkl
# List of airpots
curl --insecure 'https://ourairports.com/data/airports.csv' -O './data/raw/airports.csv'

