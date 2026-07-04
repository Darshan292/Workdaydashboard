"""
Dashboard Filter Callbacks
"""

import pandas as pd

from dash import Input, Output, State, callback


def register_filter_callbacks(app):

    @app.callback(

        Output(

            "filtered-data",

            "data"

        ),

        [

            Input(

                "date-range",

                "start_date"

            ),

            Input(

                "date-range",

                "end_date"

            ),

            Input(

                "period-filter",

                "value"

            ),

            Input(

                "integration-filter",

                "value"

            ),

            Input(

                "status-filter",

                "value"

            ),

            Input(

                "processing-slider",

                "value"

            ),

            Input(

                "items-slider",

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

        ],

        State(

            "master-data",

            "data"

        )

    )

    def filter_dashboard(

        start_date,

        end_date,

        period,

        integrations,

        statuses,

        processing_range,

        items_range,

        failure_reason,

        report_type,

        search_text,

        master_data

    ):

        if master_data is None:

            return []

        df = pd.DataFrame(

            master_data

        )

        if df.empty:

            return []

        if "event_date" in df.columns:

            df["event_date"] = pd.to_datetime(

                df["event_date"],

                errors="coerce"

            )

        # --------------------------------------------

        if start_date:

            df = df[

                df["event_date"]

                >=

                pd.to_datetime(

                    start_date

                )

            ]

        if end_date:

            df = df[

                df["event_date"]

                <=

                pd.to_datetime(

                    end_date

                )

            ]

        # --------------------------------------------

        if integrations:

            df = df[

                df["integration_system"]

                .isin(

                    integrations

                )

            ]

        # --------------------------------------------

        if statuses:

            df = df[

                df["status"]

                .isin(

                    statuses

                )

            ]

        # --------------------------------------------

        if processing_range:

            df = df[

                (

                    df["processing_time_seconds"]

                    >=

                    processing_range[0]

                )

                &

                (

                    df["processing_time_seconds"]

                    <=

                    processing_range[1]

                )

            ]

        # --------------------------------------------

        if items_range:

            df = df[

                (

                    df["items_processed"]

                    >=

                    items_range[0]

                )

                &

                (

                    df["items_processed"]

                    <=

                    items_range[1]

                )

            ]

        # --------------------------------------------

        if failure_reason:

            df = df[

                df["errors_warnings"]

                .fillna("")

                .str.contains(

                    failure_reason,

                    case=False,

                    na=False

                )

            ]

        # --------------------------------------------

        if report_type:

            df = df[

                df["report_type"]

                ==

                report_type

            ]

        # --------------------------------------------

        if search_text:

            df = df[

                df["integration_system"]

                .fillna("")

                .str.contains(

                    search_text,

                    case=False,

                    na=False

                )

            ]

        # --------------------------------------------

        if period:

            today = df["event_date"].max()

            if pd.notna(today):

                if period == "daily":

                    df = df[

                        df["event_date"]

                        >=

                        today

                        -

                        pd.Timedelta(

                            days=1

                        )

                    ]

                elif period == "weekly":

                    df = df[

                        df["event_date"]

                        >=

                        today

                        -

                        pd.Timedelta(

                            days=7

                        )

                    ]

                elif period == "monthly":

                    df = df[

                        df["event_date"]

                        >=

                        today

                        -

                        pd.Timedelta(

                            days=30

                        )

                    ]

        return df.to_dict(

            "records"

        )