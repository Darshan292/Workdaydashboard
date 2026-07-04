"""
Enterprise Live Activity Feed
"""

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from config.theme import CURRENT_THEME


class LiveActivityFeed:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    # ============================================================
    # Badge Color
    # ============================================================

    @staticmethod
    def badge(status):

        status = str(status).lower()

        if status == "success":
            return "success"

        if status == "failed":
            return "danger"

        if status == "warning":
            return "warning"

        if status == "running":
            return "primary"

        return "secondary"

    # ============================================================
    # Icon
    # ============================================================

    @staticmethod
    def icon(status):

        status = str(status).lower()

        if status == "success":
            return "✅"

        if status == "failed":
            return "❌"

        if status == "warning":
            return "⚠️"

        if status == "running":
            return "🔄"

        return "ℹ️"

    # ============================================================
    # Feed
    # ============================================================

    def build(self, limit=50):

        if self.df.empty:

            return dbc.Alert(

                "No activity available.",

                color="secondary"

            )

        data = self.df.copy()

        data["event_date"] = pd.to_datetime(

            data["event_date"],

            errors="coerce"

        )

        data = (

            data

            .sort_values(

                "event_date",

                ascending=False

            )

            .head(limit)

        )

        cards = []

        for _, row in data.iterrows():

            runtime = row.get(

                "processing_time_seconds",

                0

            )

            runtime = 0 if pd.isna(runtime) else runtime

            items = row.get(

                "items_processed",

                0

            )

            items = 0 if pd.isna(items) else items

            response = str(

                row.get(

                    "response_message",

                    ""

                )

            )[:120]

            cards.append(

                dbc.Card(

                    dbc.CardBody(

                        [

                            html.Div(

                                [

                                    html.Div(

                                        [

                                            html.Span(

                                                self.icon(

                                                    row["status"]

                                                ),

                                                style={

                                                    "fontSize": "20px",

                                                    "marginRight": "10px"

                                                }

                                            ),

                                            html.Strong(

                                                row["integration_system"]

                                            )

                                        ],

                                        className="d-flex align-items-center"

                                    ),

                                    dbc.Badge(

                                        row["status"],

                                        color=self.badge(

                                            row["status"]

                                        ),

                                        pill=True

                                    )

                                ],

                                className="d-flex justify-content-between"

                            ),

                            html.Hr(),

                            html.Div(

                                [

                                    html.Small(

                                        row.get(

                                            "integration_event",

                                            ""

                                        ),

                                        className="text-muted"

                                    )

                                ]

                            ),

                            html.Br(),

                            html.Div(

                                [

                                    html.B(

                                        "Runtime: "

                                    ),

                                    f"{runtime:.2f} sec"

                                ]

                            ),

                            html.Div(

                                [

                                    html.B(

                                        "Items: "

                                    ),

                                    f"{items:,}"

                                ]

                            ),

                            html.Div(

                                [

                                    html.B(

                                        "Time: "

                                    ),

                                    row["event_date"].strftime(

                                        "%d-%b %H:%M:%S"

                                    )

                                ]

                            ),

                            html.Br(),

                            html.Div(

                                response,

                                style={

                                    "fontSize": "13px",

                                    "color": CURRENT_THEME["secondary_text"]

                                }

                            )

                        ]

                    ),

                    className="mb-3 shadow-sm activity-card"

                )

            )

        return html.Div(

            cards,

            style={

                "maxHeight": "900px",

                "overflowY": "auto",

                "paddingRight": "6px"

            }

        )