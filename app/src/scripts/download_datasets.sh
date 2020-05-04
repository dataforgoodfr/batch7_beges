set -ex
mkdir -p /data/raw/chorus-dt
mkdir -p /data/raw/osfi
mkdir -p /data/raw/odrive
mkdir -p /data/prepared
mkdir -p /data/cleaned

#############
# Chorus DT #
#############
# Avion train sample
OUTPUT_PATH=/data/raw/chorus-dt
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=1l_DE8hWpxKtjCBpHZ_JPIkjNeyw8LQ-c' -O $OUTPUT_PATH/first_semester.zip
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=14iHwd8whxncIjy5qF-d71I8GTmgtH_p6' -O $OUTPUT_PATH/second_semester.zip
unzip -o $OUTPUT_PATH/first_semester.zip -d $OUTPUT_PATH
unzip -o $OUTPUT_PATH/second_semester.zip -d $OUTPUT_PATH

# Laposte codes
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=1EFDXoxmiXVGHwsi6aIPLXQxoMoO9y7ut' -O $OUTPUT_PATH/laposte_hexasmal.csv
# Lists of train stations
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=1zLRRqbHNH4y487JKoBA-GhfPSZt-7GhF' -O $OUTPUT_PATH/liste-des-gares.csv
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WSAj7khA-HGjTyHpWbAXzZs2JGafNkfD' -O $OUTPUT_PATH/referentiel-gares-voyageurs.csv
# Gmap cache
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1iw8q0Ve5AMusts11GrI2XzmOAbfKaclM' -O $OUTPUT_PATH/gmap_responses.pkl
# List of airpots
wget --no-check-certificate 'https://ourairports.com/data/airports.csv' -O $OUTPUT_PATH/airports.csv


#############
#   OSFI    #
#############
OUTPUT_PATH=/data/raw/osfi
wget -c --no-check-certificate 'https://docs.google.com/uc?export=download&id=1vzJKxyAi9ew0238z8IMULfX0ZPFtBqwV' -O $OUTPUT_PATH/osfi.csv
