"""
Enterprise Data Table Callbacks
"""

import pandas as pd

from dash import Input
from dash import Output
from dash import State
from dash import callback
from dash import no_update


def register_table_callbacks(app):

    @app.callback(

        [

            Output(

                "integration-table",

                "data"

            ),

            Output(

                "integration-table",

                "columns"

            )

        ],

        Input(

            "filtered-data",

            "data"

        )

    )

    def update_table(

        filtered_data

    ):

        if filtered_data is None:

            return [], []

        df = pd.DataFrame(

            filtered_data

        )

        if df.empty:

            return [], []

        columns = [

            {

                "name": column.replace(

                    "_",

                    " "

                ).title(),

                "id": column

            }

            for column in df.columns

        ]

        return (

            df.to_dict(

                "records"

            ),

            columns

        )

    # ==========================================================
    # Row Selection
    # ==========================================================

    @app.callback(

        Output(

            "notification-toast",

            "children"

        ),

        Output(

            "notification-toast",

            "is_open"

        ),

        Input(

            "integration-table",

            "selected_rows"

        ),

        State(

            "integration-table",

            "data"

        ),

        prevent_initial_call=True

    )

    def show_selected_row(

        selected,

        rows

    ):

        if not selected:

            return (

                no_update,

                False

            )

        row = rows[

            selected[0]

        ]

        message = [

            f"Integration : {row.get('integration_system','-')}",

            f"Status : {row.get('status','-')}",

            f"Runtime : {row.get('processing_time_seconds','-')} sec",

            f"Items : {row.get('items_processed','-')}"

        ]

        return (

            " | ".join(

                message

            ),

            True

        )

    # ==========================================================
    # Download Visible Data
    # ==========================================================

    @app.callback(

        Output(

            "download-dataframe",

            "data"

        ),

        Input(

            "export-table",

            "n_clicks"

        ),

        State(

            "integration-table",

            "derived_virtual_data"

        ),

        prevent_initial_call=True

    )

    def export_table(

        n_clicks,

        visible_rows

    ):

        if not n_clicks:

            return no_update

        if visible_rows is None:

            return no_update

        export_df = pd.DataFrame(

            visible_rows

        )

        return dict(

            content=export_df.to_csv(

                index=False

            ),

            filename="integration_report.csv"

        )

    # ==========================================================
    # Table Statistics
    # ==========================================================

    @app.callback(

        Output(

            "table-record-count",

            "children"

        ),

        Input(

            "integration-table",

            "derived_virtual_data"

        )

    )

    def update_record_count(

        rows

    ):

        if rows is None:

            return "0 Records"

        return (

            f"{len(rows):,} Records"

        )