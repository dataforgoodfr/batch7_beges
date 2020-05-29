import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

div_about = html.Div(
    [
        html.P("En savoir plus :"),
        html.Ul(
            [
                html.Li(dcc.Link("À propos du projet", href="/a_propos")),
                html.Li(dcc.Link("Méthodologie", href="/methodologie")),
            ],
            style={"list-style-type": "none"},
        ),
    ],
    className="mt-2",
)

div_sources = html.Div(
    [
        html.P("Ressources :"),
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
            ],
            style={"list-style-type": "none"},
        ),
    ],
    className="mt-2",
)
layout = html.Footer(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(div_about, width={"size": 3, "offset": 0}),
                    dbc.Col(div_sources, width={"size": 3, "offset": 0}),
                ]
            ),
            dbc.Row(
                dbc.Col(html.P("2020 © dataforgood", style={"text-align": "center", "margin": "1px"}), align="center")
            ),
        ],
        fluid=True,
    ),
    className="footer mt-5",
)
