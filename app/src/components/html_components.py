import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


def build_figure_container(title, id, footer):
    fig_containter = dbc.Card(
        [
            dbc.CardHeader(html.H5(title), style={"background-color": "#fff"}),
            dbc.CardBody([dbc.Col(dcc.Graph(id=id))], style={"padding": "0px"}),
            dbc.CardFooter(footer),
        ],
        className="pretty_container",
    )
    return fig_containter


def build_table_container(title, id, footer):
    fig_containter = dbc.Card(
        [
            dbc.CardHeader(html.H4(title), style={"background-color": "#fff"}),
            dbc.CardBody(
                [dbc.Col(dash_table.DataTable(id=id, style_table={"overflowX": "auto"}))], style={"padding": "0px"}
            ),
            dbc.CardFooter(footer),
        ],
        className="pretty_container",
    )
    return fig_containter


def build_card_indicateur(title, value, value_id):
    return dbc.Card(dbc.CardBody([html.P(title), html.H3(value, id=value_id)]), className="pretty_container")
