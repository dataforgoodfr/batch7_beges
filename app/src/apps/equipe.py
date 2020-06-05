
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def get_team_member_card(name, title=None, linkedin=None, github=None):
    return dbc.Card( [
        dbc.CardImg(src="/static/images/test.jpg", top=True),
        dbc.CardBody(
            [
            html.H5(name, className="card-title"),
            html.I(title),
            html.P( 'Small test', className='card-text')
            ],
            style={'text-align': 'center'}

        )
        ],
        className='m-2'
    )

layout = dbc.Row(
    dbc.Col( [
        html.H1('Les porteurs du projet', className='m-5'),
        dbc.Row( [
            dbc.Col(
                get_team_member_card(name='Anthony Dicanot'),
                width={'offset': 2, 'size': 4},
            ),
            dbc.Col(
                get_team_member_card(name='Maxime Roux'),
                width=4
            ),
        ]),
        html.Br(),
        html.H1("L'équipe technique", className='m-5'),
        dbc.Row( [
                dbc.Col(
                    get_team_member_card(name='Antoine Biard',
                    title="Data engineer / data scientist"
                    ),
                    width=4,
                ),
                dbc.Col(
                    get_team_member_card(name='Ayoub Samaki', title="Data scientist"),
                    width=4,
                ),
                dbc.Col(
                    get_team_member_card(name='Tallulah Axinn'),
                    width=4,
                ),
            ]
        ),
        dbc.Row( [
                dbc.Col(
                    get_team_member_card(name='Gustave Ronteix', title="Data scientist"),
                    width=4,
                ),
                dbc.Col(
                    get_team_member_card(name='Artus Vuatrin'),
                    width=4,
                ),
                dbc.Col(
                    get_team_member_card(name='Maria Anaya'),
                    width=4,
                ),
            ]
        ),
        dbc.Row( [
                dbc.Col(
                    get_team_member_card(name='Svetlana Bazhenova'),
                    width=4,
                ),
        ]),
    ],
    width={'size': 6, 'offset': 3}
    )
)
