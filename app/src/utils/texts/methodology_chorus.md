### Déplacements professionnels effectués en avion et train

Les émissions liées aux déplacements professionnels en avion et train sont calculées à partir de la base Chorus DT. Elles sont comprises dans le poste d'émission n°23 (Déplacements professionnels) du scope 3.

Elles sont obtenues en trois étapes :

1) La définition des points d’arrivée et de départ de façon homogène (certains trajets présentent des villes, d’autres présentent des codes IATA dans le cas de trajets effectués en avion).

2) Le calcul des distances.

3) Le croisement de ces distances aux facteurs d’émissions dédié de la base carbone, selon le moyen de transport :
- dans le cas du train, selon qu’il s’agisse d’un TGV ou d’un TER. Un biais de calcul subsiste dans le fait que la base Chorus DT n’indique pas si un trajet effectué en train l’a été en TER ou TGV. Le tri des données a été effectué à partir de la base open data de la SNCF listant les émissions de CO2 sur ses liaisons TGV (https://ressources.data.sncf.com/explore/dataset/emission-co2-tgv/table/). Les émissions restantes (en kgCO2e/passager) correspondant donc aux trajets en TER ont été obtenues en croisant les distances précédemment calculées avec le facteur d’émission associé (en kgCO2e/passager.km) de la base carbone.
- dans le cas de l’avion, la base carbone propose des facteurs d’émissions selon le type d’avion (court, moyen, long courrier) ou selon le double filtre capacité puis distance parcourue. La base Chorus DT ne donne pas d’information sur le type d’avion. Les émissions ont donc été calculées sur la base des distances parcourues. Un biais de calcul subsiste dans le fait qu’il existe plusieurs facteurs d’émission pour une même distance. Ceci est dû au fait que les intervalles de distances parcourues ne sont pas propres à une capacité d’avion (exemple : l’intervalle de distance [500 km – 1000 km] se retrouve pour les avions de capacité comprise entre 20 et 50 sièges, de même que pour les avions de capacité comprise entre 51 et 100 siège). Le choix a été fait de calculer les émissions à partir de la moyenne des facteurs d’émissions pour chaque intervalle de distance.
