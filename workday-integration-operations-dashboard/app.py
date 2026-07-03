"""
=========================================================
Workday Integration Operations Center
Enterprise Dashboard
=========================================================
"""

import dash
import dash_bootstrap_components as dbc

from config.settings import (
    APP_NAME,
    APP_VERSION
)

from config.constants import (
    REFRESH_COMPONENT
)

from layouts.dashboard import create_dashboard


# ==========================================================
# APP INITIALIZATION
# ==========================================================

app = dash.Dash(
    __name__,
    title=APP_NAME,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
    update_title=None,
)

server = app.server


# ==========================================================
# APP LAYOUT
# ==========================================================

app.layout = dbc.Container(

    [

        REFRESH_COMPONENT,

        create_dashboard(),

    ],

    fluid=True,

    className="dashboard-container"

)


# ==========================================================
# REGISTER CALLBACKS
# ==========================================================

from callbacks.filter_callbacks import register_filter_callbacks
from callbacks.chart_callbacks import register_chart_callbacks
from callbacks.table_callbacks import register_table_callbacks
from callbacks.theme_callbacks import register_theme_callbacks
from callbacks.refresh_callbacks import register_refresh_callbacks
from callbacks.sidebar_callbacks import register_sidebar_callbacks
from callbacks.kpi_callbacks import register_kpi_callbacks


register_filter_callbacks(app)
register_chart_callbacks(app)
register_table_callbacks(app)
register_theme_callbacks(app)
register_refresh_callbacks(app)
register_sidebar_callbacks(app)
register_kpi_callbacks(app)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("=" * 60)

    app.run(

        debug=True,

        host="0.0.0.0",

        port=8050

    )