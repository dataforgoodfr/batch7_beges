import dash
import os
import dash_bootstrap_components as dbc
from flask_login import LoginManager, UserMixin

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        "href": "https://use.fontawesome.com/releases/v5.8.1/css/all.css",
        "rel": "stylesheet",
        "integrity": "sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
        "crossorigin": "anonymous",
    },
]  # ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Beges"

app.config.suppress_callback_exceptions = True
app.server.config.update(SECRET_KEY=os.urandom(12))

# Setting up the login
login_manager = LoginManager()
login_manager.init_app(app.server)
login_manager.login_view = "/login"


class User(UserMixin):
    def __init__(self, name, pwd, email):
        self.id = name
        self.username = name
        self.email = email
        self.password = pwd

    def __repr__(self):
        return "User: ({name}, {pwd})".format(name=self.username, pwd=self.password)


ADMIN_NAME = os.getenv("APP_ADMIN_NAME", "admin")
ADMIN_PWD = os.getenv("APP_ADMIN_PWD", "pwd")
ADMIN_EMAIL = os.getenv("APP_ADMIN_EMAIL", "email@gmail.com")
ADMINS = {ADMIN_NAME: User(name=ADMIN_NAME, pwd=ADMIN_PWD, email=ADMIN_EMAIL)}

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return ADMINS[user_id]
