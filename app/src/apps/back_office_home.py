import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        html.H1("Backoffice"),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Gestion de l'organigramme", href="/backoffice/entities")),
                dbc.NavItem(dbc.NavLink("Dépôt de fichiers", href="/backoffice/upload_files")),
                dbc.NavItem(dbc.NavLink("Se déconnecter", href="/logout")),
            ],
            vertical="md",
        ),
    ]
)
