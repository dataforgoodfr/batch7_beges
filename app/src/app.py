import dash
import dash_html_components as html

from components import header
from components import entity_choice
from components import data_display

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.title = "Beges"
# The underlying flask server
flask_app = dash_app.server

# Registering callbacks

dash_app.layout = html.Div(children=[header.layout, html.Hr(), entity_choice.layout, html.Hr(), data_display.layout])

entity_choice.register_callbacks(dash_app)
data_display.register_callbacks(dash_app)

if __name__ == "__main__":
    dash_app.run_server(debug=True, host="0.0.0.0", port=80)
