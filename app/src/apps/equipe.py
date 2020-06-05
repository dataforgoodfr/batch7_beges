
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

class TeamMember:
    def __init__( self, full_name, image_url=None, title=None, github_link=None, linkedin_link=None, email=None):
        self.full_name = full_name
        self.image_url=image_url
        self.title = title
        self.github_link=github_link
        self.linkedin_link = linkedin_link
        self.email = email

    def get_card(self):
        card_image = dbc.CardImg(src=self.image_url, top=True)
        links = []
        if self.linkedin_link:
            links.append(dbc.CardLink(html.I(className='fab fa-linkedin fa-2x'), external_link=True, href=self.linkedin_link))
        if self.github_link:
            links.append(dbc.CardLink(html.I(className='fab fa-github fa-2x'), external_link=True, href=self.github_link))
        if self.email:
            links.append(dbc.CardLink(html.I(className='fa fa-envelope fa-2x'), external_link=True, href='mailto:' + self.email))
        card_body = dbc.CardBody(
                [
                html.H5(self.full_name, className="card-title", style={'text-align': 'center'}),
                html.Div(html.I(self.title), style={'text-align': 'center'}),
                html.Br(),
                html.Div(links, style={'display': 'inline'})
                ],
                
            )
        return dbc.Card(
            [card_image, card_body],
            className='m-2')

team_members = {}
team_members['anthony'] = TeamMember(
    full_name="Anthony Dicanot",
    title='MTES',
    image_url='https://media-exp1.licdn.com/dms/image/C4E03AQF35iIIrNzpHA/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=0Av8a_Y8LPdJ0SkGFcuWko6-0Ek6tacWPii9OqRmKFw',
    linkedin_link='https://www.linkedin.com/in/anthony-dicanot-853143a2',
    email='anthony.dicanot@developpement-durable.gouv.fr'
)
team_members['maxime'] = TeamMember(
    full_name="Maxime Roux",
    title='MTES',
    image_url='https://media-exp1.licdn.com/dms/image/C5603AQGEiBukxPHuWA/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=mmyrIE04y8C6fBaHXrUXN_k9YV8Wy9xPuHccIcxCkmY',
    linkedin_link='https://www.linkedin.com/in/maxime-roux-465927160/',
    email='maxime.roux@developpement-durable.gouv.fr'
)
team_members['antoine'] = TeamMember(
    full_name="Antoine Biard",
    title="Data engineer / data scientist",
    image_url='https://media-exp1.licdn.com/dms/image/C4E03AQFoW00Gg42s8A/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=wKbJs7eqdDJ7ly0iKV4ajq4L7BYZMgSSYZsQO5RBIcA',
    linkedin_link='https://www.linkedin.com/in/antoine-biard-02906355/',
    github_link='https://github.com/antoan2',
    email='antoine.biard.10@gmail.com'
)
team_members['artus'] = TeamMember(full_name="Artus Vuatrin", title="Data scientist", github_link='https://github.com/ArtusVuatrin', linkedin_link='https://www.linkedin.com/in/artus-vuatrin-577706124', image_url='https://media-exp1.licdn.com/dms/image/C5103AQFL2vwfNkhHAw/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=_1BaokPcTgQ16zlrLUWgyXUnf8SEr7OwhPp641QQLJA')
team_members['ayoub'] = TeamMember(full_name='Ayoub Samaki', title="Data scientist", linkedin_link='https://www.linkedin.com/in/ayoub-samaki-0a158588/', github_link='https://github.com/Tiyop', image_url='https://media-exp1.licdn.com/dms/image/C5603AQH0Y9Ts4l7odg/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=U09iFCsbpYH25kY7WR77cWiLRDdt55zuBgW_bZl-ahs')
team_members['tallulah'] = TeamMember(full_name='Tallulah Axinn', title="Data scientist", github_link='https://github.com/tallulaha', linkedin_link='https://www.linkedin.com/in/tallulah-axinn-586509a8')
team_members['gustave'] = TeamMember(full_name='Gustave Ronteix', title="Data scientist", github_link='https://github.com/gronteix', linkedin_link='https://www.linkedin.com/in/gustave-ronteix-677a82ba', image_url='https://media-exp1.licdn.com/dms/image/C5603AQFiE0RWAQ0KzQ/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=PhG6TzTxW6xvqDLfX_lRZH_iL_Sp5CUNZuQHcdHPKNo')
team_members['maria'] = TeamMember(full_name='Maria Anaya', linkedin_link='https://www.linkedin.com/in/mariaanaya/', image_url='https://media-exp1.licdn.com/dms/image/C5603AQF0PeKRRNoZWA/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=G_tAgB7Xs7Hr1mJbC-LUbs8VFUFLmOc-cMKAPL8WyhU' )
team_members['svetlana'] = TeamMember(full_name='Svetlana Bazhenova', image_url='https://media-exp1.licdn.com/dms/image/C5603AQHcVXiOBeapvg/profile-displayphoto-shrink_200_200/0?e=1596672000&v=beta&t=G7JibPanZNxvGuLb1wgRFNIpTYi4a45mP_YiNCC2V3E', linkedin_link='https://www.linkedin.com/in/svetlana-bazhenova/')

layout = dbc.Row(
    dbc.Col( [
        html.H1('Les porteurs du projet', className='m-5'),
        dbc.Row( [
            dbc.Col(
                team_members['anthony'].get_card(),
                width={'offset': 2, 'size': 4},
            ),
            dbc.Col(
                team_members['maxime'].get_card(),
                width=4
            ),
        ]),
        html.Br(),
        html.H1("L'équipe technique", className='m-5'),
        dbc.Row( [
                dbc.Col(
                    team_members['antoine'].get_card(),
                    width=4,
                ),
                dbc.Col(
                    team_members['ayoub'].get_card(),
                    width=4,
                ),
                dbc.Col(
                    team_members['tallulah'].get_card(),
                    width=4,
                ),
            ]
        ),
        dbc.Row( [
                dbc.Col(
                    team_members['gustave'].get_card(),

                    width=4,
                ),
                dbc.Col(
                    team_members['artus'].get_card(),
                    width=4,
                ),
                dbc.Col(
                    team_members['maria'].get_card(),
                    width=4,
                ),
            ]
        ),
        dbc.Row( [
                dbc.Col(
                    team_members['svetlana'].get_card(),
                    width=4,
                ),
        ]),
    ],
    width={'size': 6, 'offset': 3}
    )
)
