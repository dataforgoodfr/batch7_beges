import dash_html_components as html
import dash_core_components as dcc

intro = dcc.Markdown(
    """
# Introduction
L'objectif de cette application est de centraliser les données pour les différentes entitées... (on explique qu'on récupère les différents datasets et tout et tout)
"""
)
methodology_odrive = dcc.Markdown(
    """
# Déplacement en voiture
Et voilà, on a récupéré la base de données Odrive et puis c'est tout.
"""
)
methodology_chorus_dt = dcc.Markdown(
    """
# Déplacement en train / avion
On a récupéré la base de données Chorus dt qui centralise tout ca.
Puis on a résolu les noms d'endroit en utilisant l'API de gmap.

Et on a utilisé les facteurs d'émissions suivants :
- Facteur 1
- Facteur 2
"""
)

methodology_osfi = dcc.Markdown(
    """
# Dépenses énergétiques
On a récupéré la base de données OSFI uniquement en production ici et là.

Et on a utilisé les facteurs d'émissions suivants :
- Facteur 1
- Facteur 2
"""
)

layout = html.Div(
    children=[intro]
    + [html.A(id="methodologie_odrive"), methodology_odrive]
    + [html.A(id="methodologie_chorus_dt"), methodology_chorus_dt]
    + [html.A(id="methodologie_osfi"), methodology_osfi]
)
