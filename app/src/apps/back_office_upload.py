import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from utils.texts import TEXTS
from apps.back_office_home import get_vertical_backoffice_navbar


def get_upload_component(id, filename="test"):
    return dcc.Upload(
        id="upload-data",
        children=html.Div(
            [
                filename,
                " : Cliquer glisser le fichier ou ",
                html.A("charger un fichier", style={"color": "blue", "cursor": "pointer"}),
            ]
        ),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        # Allow multiple files to be uploaded
        multiple=False,
    )


chorus_dt_drop_files = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Chorus dt"),
            dbc.Row(
                [
                    dbc.Col(dcc.Markdown(TEXTS["backoffice_drop_chorus_dt"]), width=6),
                    dbc.Col(get_upload_component("back-office-chorus-dump", "Export Chorus-dt"), width=6),
                ]
            ),
        ]
    )
)
odrive_drop_files = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Odrive"),
            dbc.Row(
                [
                    dbc.Col(dcc.Markdown(TEXTS["backoffice_drop_odrive"]), width=6),
                    dbc.Col(get_upload_component("back-office-odrive-dump", "Export Odrive"), width=6),
                ]
            ),
        ]
    )
)
osfi_drop_files = dbc.Card(
    dbc.CardBody(
        [
            html.H4("OSFI"),
            dbc.Row(
                [
                    dbc.Col(dcc.Markdown(TEXTS["backoffice_drop_osfi"]), width=6),
                    dbc.Col(
                        [
                            dbc.Row(dbc.Col(get_upload_component("back-office-osfi-rt-dump", "Export OSFI RT"))),
                            dbc.Row(
                                dbc.Col(
                                    get_upload_component(
                                        "back-office-osfi-monthly-dump", "Export OSFI Consommations mensuelles"
                                    )
                                )
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
        ]
    )
)

layout = html.Div(
    dbc.Row(
        [
            dbc.Col(get_vertical_backoffice_navbar(), width=2),
            dbc.Col(
                [
                    html.H1("Dépôt de fichiers"),
                    html.Hr(),
                    chorus_dt_drop_files,
                    html.Hr(),
                    odrive_drop_files,
                    html.Hr(),
                    osfi_drop_files,
                ]
            ),
        ]
    )
)
