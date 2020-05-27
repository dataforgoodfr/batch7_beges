# Méthodologie
## Introduction
Actuellement, un BEGES s’articule autour de 23 postes d’émissions répartis en 3 catégories ou « scope ». 
- Scope 1 : émissions directes produites par les sources fixes et mobiles détenues par l’entité (ex : émissions du parc de véhicules de l’entité).
- Scope 2 : émissions indirectes liées à la consommation d’électricité, de vapeur, de chaleur ou de froid (consommation électrique des locaux détenus par l’entité).
- Scope 3 : autres émissions indirectes (ex : déplacements professionnels, ou encore déplacements domicile-travail des agents).

L’outil a été développé autour de trois bases de données permettant l’estimation du volume des émissions liées :
-	aux déplacements professionnels en avion et train (scope 3)
-	aux déplacements professionnels réalisés en voiture (scope 1)
-	à la consommation énergétique (gaz et électricité) des bâtiments de l’entité (scopes 1 & 2).
Le guide sectoriel de l’ADEME dédié au calcul des émissions du secteur tertiaire non marchand présente ces catégories d’émissions comme les plus pertinentes pour une administration.

_Fonctionnement_
*Centralisation des données*
La première étape est la centralisation des données de différentes bases pour une ou plusieurs entités. Cette centralisation est effectuée par chargement des exports (format .csv) des bases de données directement dans l’outil. 
Les contraintes de réalisation d’un BEGES permettent de se limiter à un chargement annuel des bases de données.

*Formatage et mise en cohérence des bases de données*
Les différentes bases ne présentent pas le même formatage des données. Des différences sont observées en termes d’identification (libellés différents, utilisation non systématique de codes d’identification), ou encore de granularité (maillage plus ou moins fin des entités et de leurs sous-entités). 
La mise en cohérence permet d’associer une entité à ses données liées et réparties dans les différentes bases. 

La mise en relation des bases de données dans l’Outil-BEGES fonctionne en 3 étapes : 

1)	La définition d’un organigramme présentant les entités souhaitées. Cet organigramme est facilement modifiable et permet l’ajout ou la suppression d’une entité, voire un changement de libellé.

2)	L’association d’un code d’identification à chaque entité, pour chaque base de données. 

3)	La mise en relation des codes de l’entité. Les codes d’une même entité sont associés dans l’outil au libellé correspondant dans l’organigramme. 

*Estimation des émissions pour chaque base de données*
Le calcul des émissions est basé sur le guide méthodologique de l’ADEME pour la réalisation des BEGES.

**Consommation énergétique des bâtiments**
Les émissions liées à la consommation énergétique des bâtiments sont calculées à partir de la base OSFi (outil de suivi des fluides). Elles sont obtenues par croisement de ces données avec le facteur d’émission correspondant : mix moyen électricité ou gaz, France continentale ou Outre-mer.

**Déplacements professionnels effectués en voiture**
Les émissions liées aux déplacements professionnels en voiture sont calculées à partir de la base ODRIVE. Elles sont obtenues par croisement de la moyenne kilométrique annuelle de chaque véhicule avec les données d’émissions de GES/km qui leur sont propres.

**Déplacements professionnels effectués en avion et train**
Les émissions liées aux déplacements professionnels en voiture sont calculées à partir de la base Chorus DT. Elles sont obtenues en trois étapes : 
1)	La définition des points d’arrivée et de départ de façon homogène (certains trajets présentent des villes, d’autres présentent des codes IATA dans le cas de trajets effectués en avion).
2)	Le calcul des distances.
3)	Le croisement de ces distances aux facteurs d’émissions dédié de la base carbone, selon le moyen de transport :
- dans le cas du train, selon qu’il s’agisse d’un TGV ou d’un TER ;
- dans le cas de l’avion, selon la distance (sur la base carbone, les facteurs d’émissions liés à un déplacement en avion sont classés par capacité et par distance).

