set -ex
# Avion train sample
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1l_DE8hWpxKtjCBpHZ_JPIkjNeyw8LQ-c' -O ./data/raw/first_semester.zip
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=14iHwd8whxncIjy5qF-d71I8GTmgtH_p6' -O ./data/raw/second_semester.zip
unzip ./data/raw/first_semester.zip -d ./data/prepared/
unzip ./data/raw/second_semester.zip -d ./data/prepared/

# Laposte codes
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1EFDXoxmiXVGHwsi6aIPLXQxoMoO9y7ut' -O ./data/raw/laposte_hexasmal.csv
# Lists of train stations
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1zLRRqbHNH4y487JKoBA-GhfPSZt-7GhF' -O ./data/raw/liste-des-gares.csv
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WSAj7khA-HGjTyHpWbAXzZs2JGafNkfD' -O ./data/raw/referentiel-gares-voyageurs.csv
# Gmap cache
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1iw8q0Ve5AMusts11GrI2XzmOAbfKaclM' -O ./data/raw/gmap_responses.pkl
# List of airpots
wget --no-check-certificate 'https://ourairports.com/data/airports.csv' -O './data/raw/airports.csv'

