import dash_html_components as html
import dash_core_components as dcc

from utils.texts import TEXTS

intro = dcc.Markdown(TEXTS["methodology_intro"])
methodology_odrive = dcc.Markdown(TEXTS["methodology_odrive"])
methodology_chorus = dcc.Markdown(TEXTS["methodology_chorus"])
methodology_osfi = dcc.Markdown(TEXTS["methodology_osfi"])

layout = html.Div(
    children=[intro]
    + [html.A(id="methodologie_odrive"), methodology_odrive]
    + [html.A(id="methodologie_chorus"), methodology_chorus]
    + [html.A(id="methodologie_osfi"), methodology_osfi]
)
