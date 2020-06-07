### Déplacements professionnels effectués en avion et train
Les émissions liées aux déplacements professionnels en avion et train sont calculées à partir de la base Chorus DT. Elles sont comprises dans le poste d'émission "Déplacements professionnels" du scope 3.

Elles sont obtenues en trois étapes :

1) La définition des points d’arrivée et de départ de façon homogène (certains trajets présentent des villes, d’autres présentent des codes IATA dans le cas de trajets effectués en avion). A chaque point de départ et d'arrivée est associé sa localisation géographique. C'est le couple de coordonnées latitude/longitude qui servira au calcul des distances parcourues.

2) Le calcul des distances.

3) Le croisement de ces distances aux facteurs d’émissions dédié de la base carbone, selon le moyen de transport :
- dans le cas du train, la base de données ne permet pas de différencier les voyages effectués en TGV de ceux effectués en TER. On choisit donc d'opter pour une estimation conservative des émissions, correspondant donc aux trajets en TER. On calcule ainsi les émissions du trajet en croisant la distance précédemment calculée avec le facteur d’émission associé au TER (en kgCO2e/passager.km) de la base carbone.
- dans le cas de l’avion, la base carbone propose des facteurs d’émissions selon le type d’avion (court, moyen, long courrier) ou selon le double filtre capacité puis distance parcourue. La base Chorus DT ne donne pas d’information sur le type d’avion. Les émissions ont donc été calculées sur la base des distances parcourues. Un biais de calcul subsiste dans le fait qu’il existe plusieurs facteurs d’émission pour une même distance. Ceci est dû au fait que les intervalles de distances parcourues ne sont pas propres à une capacité d’avion (exemple : l’intervalle de distance 500 km – 1000 km se retrouve aussi bien pour les avions de capacité comprise entre 20 et 50 sièges, que pour les avions de capacité comprise entre 51 et 100 siège). Le choix a été fait de calculer les émissions à partir de la moyenne des facteurs d’émissions pour chaque intervalle de distance.
