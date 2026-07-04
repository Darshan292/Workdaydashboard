"""
Enterprise Dashboard Header
"""

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def build_header():

    return dbc.Card(

        dbc.CardBody(

            [

                dbc.Row(

                    [

                        # =====================================================
                        # Left
                        # =====================================================

                        dbc.Col(

                            [

                                html.H2(

                                    "Workday Integration Operations Center",

                                    className="dashboard-title"

                                ),

                                html.Div(

                                    [

                                        html.Span(

                                            "Enterprise Monitoring Dashboard",

                                            className="text-muted"

                                        ),

                                        html.Span(

                                            " | ",

                                            className="mx-2"

                                        ),

                                        html.Span(

                                            id="last-refresh",

                                            children="Last Refresh : --"

                                        )

                                    ]

                                )

                            ],

                            lg=6,

                            md=12

                        ),

                        # =====================================================
                        # Right
                        # =====================================================

                        dbc.Col(

                            [

                                dbc.Row(

                                    [

                                        dbc.Col(

                                            dcc.DatePickerRange(

                                                id="date-range",

                                                display_format="DD MMM YYYY",

                                                minimum_nights=0

                                            ),

                                            width="auto"

                                        ),

                                        dbc.Col(

                                            dbc.Button(

                                                [

                                                    html.I(

                                                        className="fa-solid fa-rotate",

                                                        id="refresh-icon"

                                                    ),

                                                    " Refresh"

                                                ],

                                                id="refresh-button",

                                                color="primary",

                                                className="me-2"

                                            ),

                                            width="auto"

                                        ),

                                        dbc.Col(

                                            dbc.Button(

                                                [

                                                    html.I(

                                                        className="fa-solid fa-moon me-2"

                                                    ),

                                                    html.Span(

                                                        "Dark Mode"

                                                    )

                                                ],

                                                id="theme-toggle",

                                                color="secondary"

                                            ),

                                            width="auto"

                                        )

                                    ],

                                    justify="end",

                                    className="g-2"

                                )

                            ],

                            lg=6,

                            md=12,

                            className="text-end"

                        )

                    ],

                    align="center"

                ),

                html.Hr(),

                dbc.Row(

                    [

                        dbc.Col(

                            dbc.Badge(

                                "Running",

                                id="refresh-status",

                                color="success"

                            ),

                            width="auto"

                        ),

                        dbc.Col(

                            html.Div(

                                [

                                    html.Strong("Refresh Count : "),

                                    html.Span(

                                        "0",

                                        id="refresh-count"

                                    )

                                ]

                            ),

                            width="auto"

                        ),

                        dbc.Col(

                            html.Div(

                                [

                                    html.Strong("Theme : "),

                                    html.Span(

                                        "Dark",

                                        id="theme-indicator"

                                    )

                                ]

                            ),

                            width="auto"

                        ),

                        dbc.Col(

                            dbc.Progress(

                                id="refresh-progress",

                                value=100,

                                striped=True,

                                animated=True,

                                style={

                                    "height":"8px",

                                    "marginTop":"10px"

                                }

                            )

                        ),

                        dbc.Col(

                            dbc.Switch(

                                id="auto-refresh-toggle",

                                value=True,

                                label="Auto Refresh"

                            ),

                            width="auto"

                        )

                    ],

                    className="mt-2",

                    align="center"

                )

            ]

        ),

        className="dashboard-header"

    )