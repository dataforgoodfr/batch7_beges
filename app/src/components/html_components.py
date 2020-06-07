import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def build_figure_container(title, id, footer=None):
    fig_containter = dbc.Card(
        [
            dbc.CardHeader(html.H4(title)),
            dbc.CardBody(
                [
                    dbc.Col(
                        dcc.Graph(
                            id=id,
                            config={"displaylogo": False, "toImageButtonOptions": {"filename": id, "format": "jpeg"},},
                        )
                    )
                ]
            ),
            dbc.CardFooter(footer),
        ],
        className="m-2 pretty_container",
    )
    return fig_containter


def build_table_container(title, id, footer=None):
    fig_containter = dbc.Card(
        [
            dbc.CardHeader(html.H4(title)),
            dbc.CardBody(
                [
                    dash_table.DataTable(
                        id=id, style_table={"overflowX": "auto"}, css=[{"selector": ".row", "rule": "margin: 0"}]
                    )
                ]
            ),
            dbc.CardFooter(footer),
        ],
        className="m-2 pretty_container",
    )
    return fig_containter


def build_card_indicateur(title, value, id=None):
    return dbc.Card(dbc.CardBody([html.P(title), html.H3(id=id, children=value)]), className="m-2 pretty_container")
