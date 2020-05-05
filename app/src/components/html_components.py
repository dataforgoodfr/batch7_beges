import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def build_figure_container(title, id, footer, fig=go.Figure()):
    fig_containter = dbc.Card(
        [
            dbc.CardHeader(html.H4(title), style={"background-color": "#fff"}),
            dbc.CardBody([dbc.Col(dcc.Graph(id=id, figure=fig))], style={"padding": "0px"}),
            dbc.CardFooter(footer),
        ],
        className="pretty_container",
    )
    return fig_containter


class indicator_card:
    def __init__(self, title, value):
        self.title = title
        self.value = value
        self.card = dbc.Card(dbc.CardBody([html.P(title), html.H3(value)]), className="pretty_container")

    def update_value(self, new_value):
        self.card = dbc.Card(dbc.CardBody([html.P(self.title), html.H3(new_value)]), className="pretty_container")
