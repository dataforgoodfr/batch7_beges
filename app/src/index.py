import dash
import dash_html_components as html
import dash_core_components as dcc

from components import home
from components import datasets

from app import app

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.H1("Outil d'aide à la création de BEGES", style={"text-align": "center", "margin-top": "5%"}),
        html.Hr(),
        html.Div(id="page-content"),
    ]
)

# Update the index
@app.callback(dash.dependencies.Output("page-content", "children"), [dash.dependencies.Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/datasets":
        return datasets.layout


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=80)
