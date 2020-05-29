import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from utils.texts import TEXTS

layout = dbc.Row(dbc.Col(html.Div(dcc.Markdown(TEXTS["about"])), width={"size": 6, "offset": 3}), className="mt-5")
