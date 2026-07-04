"""
Workday Integration Operations Center
Application Entry Point
"""

import dash
import dash_bootstrap_components as dbc

from config.settings import DEBUG, PORT

from services.excel_parser import ExcelParser
from services.data_cleaner import DataCleaner
from services.data_merger import DataMerger

from layouts.dashboard import DashboardLayout

from callbacks.filter_callbacks import register_filter_callbacks
from callbacks.chart_callbacks import register_chart_callbacks
from callbacks.table_callbacks import register_table_callbacks
from callbacks.theme_callbacks import register_theme_callbacks
from callbacks.refresh_callbacks import register_refresh_callbacks
from callbacks.sidebar_callbacks import register_sidebar_callbacks
from callbacks.kpi_callbacks import register_kpi_callbacks


# ============================================================
# Dash App
# ============================================================

app = dash.Dash(

    __name__,

    title="Workday Integration Operations Center",

    suppress_callback_exceptions=True,

    external_stylesheets=[

        dbc.themes.BOOTSTRAP,

        dbc.icons.FONT_AWESOME

    ],

    assets_folder="assets"

)

server = app.server

from flask import request
print("server below")

@server.before_request
def log_requests():
    print(f"{request.method} {request.path}")


# ============================================================
# Load Data
# ============================================================

parser = ExcelParser()

raw_data = parser.load_all()

cleaned_data = {

    name: DataCleaner(

        dataframe

    ).clean()

    for name, dataframe

    in raw_data.items()

}

master_dataframe = DataMerger(

    cleaned_data

).merge()


print("\n========== DATA SUMMARY ==========")

print("Master shape:", master_dataframe.shape)

print("\nColumns:")
print(master_dataframe.columns.tolist())

print("\nStatus counts:")
print(master_dataframe["status"].value_counts(dropna=False))

print("\nSource counts:")
if "source" in master_dataframe.columns:
    print(master_dataframe["source"].value_counts())

print("\nFailed rows:")
print(
    master_dataframe[
        master_dataframe["status"] == "Failed"
    ][
        [
            "integration_event",
            "status"
        ]
    ].head(20)
)

print("==================================")

# ============================================================
# Layout
# ============================================================
print("Building dashboard...")

app.layout = DashboardLayout(

    master_dataframe

).build()

print("Dashboard built.")


# ============================================================
# Register Callbacks
# ============================================================

register_filter_callbacks(

    app

)

register_chart_callbacks(

    app

)

register_table_callbacks(

    app

)

register_theme_callbacks(

    app

)

register_refresh_callbacks(

    app

)

register_sidebar_callbacks(

    app

)

register_kpi_callbacks(

    app

)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    @server.route("/health")
    def health():
        return "OK"

    app.run(

        debug= DEBUG,

        host="0.0.0.0",

        port=PORT

    )