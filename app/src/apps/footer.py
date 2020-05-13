import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

layout = html.Footer(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.P("En savoir plus :"),
                            html.Ul(
                                [
                                    html.Li(dcc.Link("À propos du projet", href="a_propos")),
                                    html.Li(dcc.Link("Méthodologie", href="methodologie")),
                                ],
                                style={"list-style-type": "none"},
                            ),
                        ],
                        style={"margin": "20px"},
                    ),
                    width={"size": 4},
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.P("Sources :"),
                            html.Ul(
                                [
                                    html.Li(
                                        dcc.Link(
                                            "Qu'est ce qu'un BEGES ?",
                                            href="https://www.bilans-ges.ademe.fr/fr/accueil/contenu/index/page/principes/siGras/0",
                                        )
                                    ),
                                    html.Li(
                                        dcc.Link(
                                            "Recommandations du gouvernment",
                                            href="https://www.ecologique-solidaire.gouv.fr/sites/default/files/Guide%20m%C3%A9thodologique%20sp%C3%A9cifique%20pour%20les%20collectivit%C3%A9s%20pour%20la%20r%C3%A9alisation%20du%20bilan%20d%E2%80%99%C3%A9missions%20de%20GES_0.pdf",
                                        )
                                    ),
                                ]
                            ),
                        ],
                        style={"margin": "20px"},
                    ),
                    width={"size": 4, "offset": 4},
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.P("2020 copyright dataforgood", style={"text-align": "center", "margin": "20px"}), align="center"
            )
        ),
    ],
    style={"background": "lightgrey", "margin": "0px"},
)
