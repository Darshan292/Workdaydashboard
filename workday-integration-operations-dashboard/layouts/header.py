"""
Enterprise Dashboard Header
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

from config.settings import APP_NAME


def create_header():

    return dbc.Card(

        dbc.CardBody(

            dbc.Row(

                [

                    # ======================================================
                    # Title
                    # ======================================================

                    dbc.Col(

                        [

                            html.Div(

                                [

                                    html.I(

                                        className="bi bi-speedometer2 dashboard-logo"

                                    ),

                                    html.Div(

                                        [

                                            html.H2(

                                                APP_NAME,

                                                className="dashboard-title"

                                            ),

                                            html.P(

                                                "Enterprise Monitoring Platform",

                                                className="dashboard-subtitle"

                                            )

                                        ]

                                    )

                                ],

                                className="header-title"

                            )

                        ],

                        lg=4,

                        md=12

                    ),

                    # ======================================================
                    # Date Range
                    # ======================================================

                    dbc.Col(

                        [

                            html.Label(

                                "Date Range",

                                className="header-label"

                            ),

                            dcc.DatePickerRange(

                                id="date-range-picker",

                                display_format="DD MMM YYYY",

                                className="date-picker"

                            )

                        ],

                        lg=3,

                        md=6

                    ),

                    # ======================================================
                    # Auto Refresh
                    # ======================================================

                    dbc.Col(

                        [

                            html.Label(

                                "Refresh",

                                className="header-label"

                            ),

                            dbc.InputGroup(

                                [

                                    dbc.InputGroupText(

                                        html.I(

                                            className="bi bi-arrow-repeat"

                                        )

                                    ),

                                    dbc.Select(

                                        id="refresh-interval",

                                        options=[

                                            {

                                                "label": "30 Seconds",

                                                "value": 30

                                            },

                                            {

                                                "label": "1 Minute",

                                                "value": 60

                                            },

                                            {

                                                "label": "5 Minutes",

                                                "value": 300

                                            },

                                            {

                                                "label": "10 Minutes",

                                                "value": 600

                                            }

                                        ],

                                        value=60

                                    )

                                ]

                            )

                        ],

                        lg=2,

                        md=6

                    ),

                    # ======================================================
                    # Right Controls
                    # ======================================================

                    dbc.Col(

                        [

                            html.Div(

                                [

                                    html.Div(

                                        [

                                            html.Small(

                                                "Last Refresh",

                                                className="refresh-label"

                                            ),

                                            html.Div(

                                                id="last-refresh",

                                                className="refresh-time"

                                            )

                                        ]

                                    ),

                                    dbc.Button(

                                        html.I(

                                            className="bi bi-arrow-clockwise"

                                        ),

                                        id="manual-refresh",

                                        color="primary",

                                        outline=True,

                                        className="refresh-button"

                                    ),

                                    dbc.Switch(

                                        id="theme-toggle",

                                        label="Dark",

                                        value=False,

                                        className="theme-switch"

                                    )

                                ],

                                className="header-actions"

                            )

                        ],

                        lg=3,

                        md=12,

                        className="text-end"

                    )

                ],

                align="center"

            )

        ),

        className="header-card shadow-sm"

    )