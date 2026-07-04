"""
Refresh Callbacks
"""

from datetime import datetime

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update

from services.excel_parser import ExcelParser
from services.data_cleaner import DataCleaner
from services.data_merger import DataMerger


def register_refresh_callbacks(app):

    # ============================================================
    # Auto / Manual Refresh
    # ============================================================

    @app.callback(

        [

            Output(

                "master-data",

                "data"

            ),

            Output(

                "last-refresh",

                "children"

            ),

            Output(

                "notification-toast",

                "children",

                allow_duplicate=True

            ),

            Output(

                "notification-toast",

                "header",

                allow_duplicate=True

            ),

            Output(

                "notification-toast",

                "icon",

                allow_duplicate=True

            ),

            Output(

                "notification-toast",

                "is_open",

                allow_duplicate=True

            )

        ],

        [

            Input(

                "auto-refresh",

                "n_intervals"

            ),

            Input(

                "refresh-button",

                "n_clicks"

            )

        ],

        prevent_initial_call=True

    )

    def refresh_dashboard(

        interval,

        button_click

    ):

        parser = ExcelParser()

        raw_frames = parser.load_all()

        cleaned = {

            name: DataCleaner(

                frame

            ).clean()

            for name, frame

            in raw_frames.items()

        }

        merged = DataMerger(

            cleaned

        ).merge()

        refresh_time = datetime.now().strftime(

            "%d %b %Y  %H:%M:%S"

        )

        return (

            merged.to_dict(

                "records"

            ),

            f"Last Refresh : {refresh_time}",

            "Dashboard refreshed successfully.",

            "Refresh Completed",

            "success",

            True

        )

    # ============================================================
    # Refresh Animation
    # ============================================================

    @app.callback(

        Output(

            "refresh-icon",

            "className"

        ),

        [

            Input(

                "refresh-button",

                "n_clicks"

            ),

            Input(

                "auto-refresh",

                "n_intervals"

            )

        ]

    )

    def rotate_refresh_icon(

        button,

        interval

    ):

        return (

            "fa-solid fa-rotate refresh-spin"

        )

    # ============================================================
    # Refresh Counter
    # ============================================================

    @app.callback(

        Output(

            "refresh-count",

            "children"

        ),

        Input(

            "auto-refresh",

            "n_intervals"

        )

    )

    def update_counter(

        count

    ):

        return f"{count:,}"

    # ============================================================
    # Auto Refresh Status
    # ============================================================

    @app.callback(

        Output(

            "refresh-status",

            "children"

        ),

        Input(

            "auto-refresh",

            "disabled"

        )

    )

    def refresh_status(

        disabled

    ):

        if disabled:

            return "Paused"

        return "Running"

    # ============================================================
    # Toggle Auto Refresh
    # ============================================================

    @app.callback(

        [

            Output(

                "auto-refresh",

                "disabled"

            ),

            Output(

                "auto-refresh-toggle",

                "children"

            )

        ],

        Input(

            "auto-refresh-toggle",

            "value"

        )

    )

    def toggle_refresh(

        enabled

    ):

        if enabled:

            return (

                False,

                "Auto Refresh ON"

            )

        return (

            True,

            "Auto Refresh OFF"

        )

    # ============================================================
    # Refresh Progress
    # ============================================================

    @app.callback(

        Output(

            "refresh-progress",

            "value"

        ),

        Input(

            "auto-refresh",

            "n_intervals"

        )

    )

    def refresh_progress(

        interval

    ):

        return 100