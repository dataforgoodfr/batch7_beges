import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from flask_login import current_user, logout_user

from apps import home
from apps import dashboard
from apps import entity_choice
from apps import about
from apps import methodology
from apps import footer
from apps import back_office_home
from apps import back_office_entities
from apps import back_office_upload
from apps import back_office_login
from apps import back_office_logout
from apps import team

from app import app


navbar = dbc.Navbar(
    [dbc.NavbarBrand("Outil d'aide à la réalisation de Bilans d'Émissions de Gaz à Effet de Serre (BEGES)", href="/")],
    color="dark",
    dark=True,
    className="nav_bar mb-3",
)

app.layout = html.Div(
    [
        html.Div(
            id="wrap",
            children=dbc.Container(
                id="main",
                children=[
                    html.Div(id="hidden_div_for_redirect_callback"),
                    dcc.Location(id="url", refresh=False),
                    navbar,
                    html.Div(id="page-content"),
                ],
                fluid=True,
                className="clear-top",
            ),
        ),
        footer.layout,
    ]
)


flask_app = app.server

# Update the index
@app.callback(
    [Output("page-content", "children"), Output("hidden_div_for_redirect_callback", "children")],
    [Input("url", "pathname")],
)
def display_page(pathname):
    # This component will be used to redirect to the home in the following situations
    #   - The url doesn't exists
    #   - The user is not connected and try to connect to the backoffice
    #   - The user just logged out
    home_redirection = dcc.Location(pathname="/", id="someid_doesnt_matter")
    backoffice_redirection = dcc.Location(pathname="/backoffice", id="someid_doesnt_matter")
    # Front end of the application
    if pathname == "/":
        return home.layout, ""
    elif pathname == "/selection_entite":
        return entity_choice.layout, ""
    elif isinstance(pathname, str) and pathname.startswith("/tableau_de_bord/"):
        return dashboard.layout, ""
    elif pathname == "/a_propos":
        return about.layout, ""
    elif pathname == "/equipe":
        return team.layout, ""
    elif pathname == "/methodologie":
        return methodology.layout, ""
    # Only root to allow login
    elif pathname == "/beegees":
        if not current_user.is_authenticated:
            return back_office_login.layout, ""
        else:
            return "", backoffice_redirection
    elif isinstance(pathname, str) and pathname.startswith("/backoffice"):
        if not current_user.is_authenticated:
            return "", home_redirection
        # Backend paths
        elif pathname == "/backoffice":
            return back_office_home.layout, ""
        elif pathname == "/backoffice/entities":
            return back_office_entities.layout, ""
        elif pathname == "/backoffice/upload_files":
            return back_office_upload.layout, ""
        else:
            return "", home_redirection
    # Logout path, will automatically redirect to the home page
    elif pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
        return "", home_redirection
    else:
        return "", home_redirection


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=80)
