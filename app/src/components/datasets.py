import dash_html_components as html

from components import entity_choice
from components import data_display

layout = html.Div(children=[entity_choice.layout, html.Hr(), data_display.layout])
