import dash
import dash_html_components as html
import dash_core_components as dcc

from components import home
from components import datasets

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Beges"
# The underlying flask server
flask_app = app.server

app.config.suppress_callback_exceptions = True


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=80)
