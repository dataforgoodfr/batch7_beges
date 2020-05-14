import dash_html_components as html
import dash_core_components as dcc


text = """
Cette application a été implémenté dans le cadre de ...
L'équipe :
- Personne 1
- Personne 2
- Personne 3
- Personne 4
"""
layout = html.Div(dcc.Markdown(text))
