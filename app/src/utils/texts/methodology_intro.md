## Introduction
Actuellement, un BEGES s’articule autour de 23 postes d’émissions répartis en 3 catégories ou « scope ».
- Scope 1 : émissions directes produites par les sources fixes et mobiles détenues par l’entité (ex : émissions du parc de véhicules de l’entité).
- Scope 2 : émissions indirectes liées à la consommation d’électricité, de vapeur, de chaleur ou de froid (consommation électrique des locaux détenus par l’entité).
- Scope 3 : autres émissions indirectes (ex : déplacements professionnels, ou encore déplacements domicile-travail des agents).

L’outil a été développé autour de trois bases de données permettant l’estimation du volume des émissions liées :
- aux déplacements professionnels en avion et train (scope 3)
- aux déplacements professionnels réalisés en voiture (scope 1)
- à la consommation énergétique (gaz et électricité) des bâtiments de l’entité (scopes 1 & 2).

Le guide sectoriel de l’ADEME dédié au calcul des émissions du secteur tertiaire non marchand présente ces catégories d’émissions comme les plus pertinentes pour une administration.

## Fonctionnement
### Centralisation des données
La première étape est la centralisation des données de différentes bases pour une ou plusieurs entités. Cette centralisation est effectuée par chargement des exports (format .csv) des bases de données directement dans l’outil.

Les contraintes de réalisation d’un BEGES permettent de se limiter à un chargement annuel des bases de données.

### Formatage et mise en cohérence des bases de données
Les différentes bases ne présentent pas le même formatage des données. Des différences sont observées en termes d’identification (libellés différents, utilisation non systématique de codes d’identification), ou encore de granularité (maillage plus ou moins fin des entités et de leurs sous-entités).

La mise en cohérence permet d’associer une entité à ses données liées et réparties dans les différentes bases.

La mise en relation des bases de données dans l’Outil-BEGES fonctionne en 3 étapes :

1) La définition d’un organigramme présentant les entités souhaitées. Cet organigramme est facilement modifiable et permet l’ajout ou la suppression d’une entité, voire un changement de libellé.
2) L’association d’un code d’identification à chaque entité, pour chaque base de données.
3) La mise en relation des codes de l’entité. Les codes d’une même entité sont associés dans l’outil au libellé correspondant dans l’organigramme.

## Estimation des émissions pour chaque base de données
Le calcul des émissions est basé sur le guide méthodologique de l’ADEME pour la réalisation des BEGES.
