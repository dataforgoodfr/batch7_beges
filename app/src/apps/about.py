import dash_html_components as html
import dash_core_components as dcc
from utils.texts import TEXTS

layout = html.Div(dcc.Markdown(TEXTS["about"]))
