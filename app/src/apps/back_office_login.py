import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app, ADMINS
from flask_login import login_user
from werkzeug.security import check_password_hash

username_input = dbc.FormGroup(
    [dbc.Label("Entrer votre nom d'administrateur"), dbc.Input(placeholder="Nom", type="text", id="uname-box")]
)

pwd_input = dbc.FormGroup(
    [dbc.Label("Entrer votre mot de passe"), dbc.Input(placeholder="Mot de passe", type="password", id="pwd-box")]
)
layout = html.Div(
    [
        dcc.Location(id="url_login", refresh=True),
        dbc.Row(
            dbc.Col(
                dbc.Form(
                    [
                        dbc.Alert(
                            "Nom d'utilisateur ou mot de passe incorrect",
                            id="output-state",
                            color="danger",
                            dismissable=True,
                            duration=5000,
                        ),
                        username_input,
                        pwd_input,
                        dbc.Button(children="Login", id="login-button", color="primary", block=True),
                    ]
                ),
                width={"size": 4, "offset": 4},
            )
        ),
    ]
)


@app.callback(
    Output("url_login", "pathname"),
    [Input("login-button", "n_clicks")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def sucess(n_clicks, input1, input2):
    if input1 in ADMINS:
        user = ADMINS[input1]
        if user.password == input2:
            login_user(user)
            return "/backoffice"
        else:
            pass
    else:
        pass


@app.callback(
    Output("output-state", "is_open"),
    [Input("login-button", "n_clicks")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def update_output(n_clicks, input1, input2):
    if n_clicks:
        if input1 in ADMINS:
            user = ADMINS[input1]
            if user.password == input2:
                return False
            else:
                return True
        else:
            return True
    else:
        return False
