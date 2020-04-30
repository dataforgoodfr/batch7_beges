import dash_html_components as html

layout = html.Div(
    id="div-header",
    children=[
        html.H1("Outil d'aide à la création de BEGES", style={"text-align": "center"}),
        html.Hr(),
        html.P(
            "Cet outil a été crée dans le crade de la saison 7 de data4good afin d'aider les différents services à créer leur Bilans d'émission de gaz à effet de serre (BEGES).",
            style={"text-align": "center"},
        ),
        html.P(
            "Différentes bases de données internes aux administrations, et identifiées comme principaux postes d'émissions de gaz à effet de serre sont exploitées.",
            style={"text-align": "center"},
        ),
        html.Ul(
            [
                html.Li("Chorus-dt: déplacements contenant des trajets en train et avion"),
                html.Li("OSFI: dépenses énergétiques des batiments"),
                html.Li("O-Drive: déplacements en voiture"),
            ],
            style={"width": "50%", "margin": "auto"},
        ),
    ],
)
