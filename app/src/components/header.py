import dash_html_components as html

layout = html.Div(
    id="div-header",
    children=[
        html.H1("Outil d'aide à la création de BEGES", style={"text-align": "center"}),
        html.Hr(),
        html.Div(
            children=[
                html.P(
                    "Cet outil a été créé dans le crade de la saison 7 de data4good afin d'aider les différents services à créer leur Bilans d'émission de gaz à effet de serre (BEGES).",
                    style={"text-align": "center"},
                ),
                html.P(
                    "Cette application permet d'exploiter les principaux postes d'émissions de gaz à effet de serre detéctés :",
                    style={"text-align": "center"},
                ),
                html.Ul(
                    [
                        html.Li("Déplacements en train / avion,"),
                        html.Li("Déplacements en voiture,"),
                        html.Li("Dépenses énergétiques des batiments."),
                    ],
                    style={"width": "50%", "margin": "auto"},
                ),
            ],
            style={"margin": "auto", "width": "50%"},
        ),
    ],
)
