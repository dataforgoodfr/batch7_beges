import dash_html_components as html

from apps import entity_choice
from apps import data_display

layout = html.Div(children=[entity_choice.layout, html.Hr(), data_display.layout])
