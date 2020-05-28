import dash_html_components as html
import dash_bootstrap_components as dbc


def get_vertical_backoffice_navbar():
    nav_items = {
        "organization_chart": dbc.NavItem(dbc.NavLink("Gestion de l'organigramme", href="/backoffice/entities")),
        "upload_files": dbc.NavItem(dbc.NavLink("Dépôt de fichiers", href="/backoffice/upload_files")),
        "logout": dbc.NavItem(dbc.NavLink("Se déconnecter", href="/logout")),
    }
    return html.Div(
        [
            dbc.Row(dbc.Col(html.H4("Backoffice", className="m-1"))),
            dbc.Row(dbc.Col(dbc.Nav([i for i in nav_items.values()], vertical="md", pills=True))),
        ],
        style={"border": "solid"},
    )


layout = html.Div(dbc.Col(get_vertical_backoffice_navbar(), width=2))
