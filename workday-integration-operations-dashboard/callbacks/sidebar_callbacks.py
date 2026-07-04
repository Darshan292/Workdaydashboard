"""
Sidebar Callbacks
"""

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update


def register_sidebar_callbacks(app):

    # ============================================================
    # Collapse / Expand Sidebar
    # ============================================================

    @app.callback(

        [

            Output(

                "sidebar",

                "className"

            ),

            Output(

                "sidebar-toggle",

                "children"

            ),

            Output(

                "sidebar-state",

                "data"

            )

        ],

        Input(

            "sidebar-toggle",

            "n_clicks"

        ),

        State(

            "sidebar-state",

            "data"

        ),

        prevent_initial_call=True

    )

    def toggle_sidebar(

        clicks,

        collapsed

    ):

        collapsed = not bool(

            collapsed

        )

        if collapsed:

            return (

                "sidebar collapsed",

                "☰",

                True

            )

        return (

            "sidebar expanded",

            "✖",

            False

        )

    # ============================================================
    # Reset Filters
    # ============================================================

    @app.callback(

        [

            Output(

                "date-range",

                "start_date"

            ),

            Output(

                "date-range",

                "end_date"

            ),

            Output(

                "integration-filter",

                "value"

            ),

            Output(

                "status-filter",

                "value"

            ),

            Output(

                "processing-slider",

                "value"

            ),

            Output(

                "items-slider",

                "value"

            ),

            Output(

                "failure-filter",

                "value"

            ),

            Output(

                "report-filter",

                "value"

            ),

            Output(

                "search-integration",

                "value"

            )

        ],

        Input(

            "reset-filters",

            "n_clicks"

        ),

        prevent_initial_call=True

    )

    def reset_filters(

        clicks

    ):

        return (

            None,

            None,

            [],

            [],

            [0, 1000],

            [0, 1000000],

            None,

            None,

            ""

        )

    # ============================================================
    # Active Filter Count
    # ============================================================

    @app.callback(

        Output(

            "active-filter-count",

            "children"

        ),

        [

            Input(

                "integration-filter",

                "value"

            ),

            Input(

                "status-filter",

                "value"

            ),

            Input(

                "failure-filter",

                "value"

            ),

            Input(

                "report-filter",

                "value"

            ),

            Input(

                "search-integration",

                "value"

            )

        ]

    )

    def update_filter_count(

        integrations,

        status,

        failure,

        report,

        search

    ):

        count = 0

        if integrations:

            count += 1

        if status:

            count += 1

        if failure:

            count += 1

        if report:

            count += 1

        if search:

            count += 1

        return f"{count} Active"

    # ============================================================
    # Search Box Clear Button
    # ============================================================

    @app.callback(

        Output(

            "search-integration",

            "value",

            allow_duplicate=True

        ),

        Input(

            "clear-search",

            "n_clicks"

        ),

        prevent_initial_call=True

    )

    def clear_search(

        clicks

    ):

        return ""

    # ============================================================
    # Sidebar Badge
    # ============================================================

    @app.callback(

        Output(

            "filter-badge",

            "children"

        ),

        Input(

            "active-filter-count",

            "children"

        )

    )

    def update_badge(

        text

    ):

        return text

    # ============================================================
    # Sidebar Width
    # ============================================================

    @app.callback(

        Output(

            "sidebar-container",

            "style"

        ),

        Input(

            "sidebar-state",

            "data"

        )

    )

    def sidebar_width(

        collapsed

    ):

        if collapsed:

            return {

                "width": "80px",

                "transition": "0.35s"

            }

        return {

            "width": "320px",

            "transition": "0.35s"

        }