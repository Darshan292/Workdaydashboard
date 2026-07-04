"""
Theme Callbacks
"""

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update


def register_theme_callbacks(app):

    # ============================================================
    # Theme Toggle
    # ============================================================

    @app.callback(

        [

            Output(

                "theme-store",

                "data"

            ),

            Output(

                "theme-toggle",

                "children"

            )

        ],

        Input(

            "theme-toggle",

            "n_clicks"

        ),

        State(

            "theme-store",

            "data"

        ),

        prevent_initial_call=True

    )

    def toggle_theme(

        n_clicks,

        current_theme

    ):

        if current_theme == "dark":

            return (

                "light",

                "🌙 Dark Mode"

            )

        return (

            "dark",

            "☀️ Light Mode"

        )

    # ============================================================
    # Dashboard Theme Class
    # ============================================================

    @app.callback(

        Output(

            "dashboard-root",

            "className"

        ),

        Input(

            "theme-store",

            "data"

        )

    )

    def update_dashboard_theme(

        theme

    ):

        if theme == "light":

            return (

                "dashboard-root light-theme"

            )

        return (

            "dashboard-root dark-theme"

        )

    # ============================================================
    # Theme Toast
    # ============================================================

    @app.callback(

        [

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

        Input(

            "theme-store",

            "data"

        ),

        prevent_initial_call=True

    )

    def theme_notification(

        theme

    ):

        if theme == "dark":

            return (

                "Dark theme enabled.",

                "Theme Updated",

                "primary",

                True

            )

        return (

            "Light theme enabled.",

            "Theme Updated",

            "success",

            True

        )

    # ============================================================
    # Theme Indicator
    # ============================================================

    @app.callback(

        Output(

            "theme-indicator",

            "children"

        ),

        Input(

            "theme-store",

            "data"

        )

    )

    def update_theme_indicator(

        theme

    ):

        if theme == "dark":

            return "Dark"

        return "Light"

    # ============================================================
    # Persist Theme
    # ============================================================

    @app.callback(

        Output(

            "theme-persistence",

            "data"

        ),

        Input(

            "theme-store",

            "data"

        )

    )

    def persist_theme(

        theme

    ):

        return theme