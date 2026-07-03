"""
Enterprise Filter Sidebar
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_sidebar():

    return dbc.Card(

        [

            dbc.CardHeader(

                [

                    html.I(className="bi bi-funnel-fill me-2"),

                    html.Span("Filters")

                ],

                className="sidebar-header"

            ),

            dbc.CardBody(

                [

                    # =====================================================
                    # Search
                    # =====================================================

                    html.Div(

                        [

                            html.Label(
                                "Search Integration",
                                className="filter-label"
                            ),

                            dbc.Input(

                                id="search-integration",

                                type="text",

                                placeholder="Search Integration...",

                                debounce=True,

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Date Mode
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "View",

                                className="filter-label"

                            ),

                            dbc.RadioItems(

                                id="period-filter",

                                options=[

                                    {

                                        "label": "Daily",

                                        "value": "Daily"

                                    },

                                    {

                                        "label": "Weekly",

                                        "value": "Weekly"

                                    },

                                    {

                                        "label": "Monthly",

                                        "value": "Monthly"

                                    }

                                ],

                                value="Daily",

                                inline=True

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Status
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "Execution Status",

                                className="filter-label"

                            ),

                            dcc.Dropdown(

                                id="status-filter",

                                options=[

                                    {

                                        "label": "All",

                                        "value": "All"

                                    },

                                    {

                                        "label": "Success",

                                        "value": "Success"

                                    },

                                    {

                                        "label": "Failed",

                                        "value": "Failed"

                                    },

                                    {

                                        "label": "Warning",

                                        "value": "Warning"

                                    },

                                    {

                                        "label": "Running",

                                        "value": "Running"

                                    }

                                ],

                                value="All",

                                clearable=False

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Report Type
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "Report Type",

                                className="filter-label"

                            ),

                            dcc.Dropdown(

                                id="report-filter",

                                options=[

                                    {

                                        "label": "All",

                                        "value": "All"

                                    },

                                    {

                                        "label": "Failures",

                                        "value": "Failures"

                                    },

                                    {

                                        "label": "Event Statistics",

                                        "value": "Event Statistics"

                                    },

                                    {

                                        "label": "Processing Time",

                                        "value": "Processing Time"

                                    }

                                ],

                                value="All",

                                clearable=False

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Processing Time
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "Processing Time (Seconds)",

                                className="filter-label"

                            ),

                            dcc.RangeSlider(

                                id="processing-slider",

                                min=0,

                                max=300,

                                step=1,

                                value=[0, 300],

                                tooltip={

                                    "placement": "bottom",

                                    "always_visible": False

                                }

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Items Processed
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "Items Processed",

                                className="filter-label"

                            ),

                            dcc.RangeSlider(

                                id="items-slider",

                                min=0,

                                max=100000,

                                step=100,

                                value=[0, 100000],

                                tooltip={

                                    "placement": "bottom"

                                }

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Failure Keyword
                    # =====================================================

                    html.Div(

                        [

                            html.Label(

                                "Failure Keyword",

                                className="filter-label"

                            ),

                            dbc.Input(

                                id="failure-filter",

                                placeholder="Timeout / Auth / Network ...",

                                debounce=True

                            )

                        ],

                        className="filter-group"

                    ),

                    html.Hr(),

                    # =====================================================
                    # Slow Executions
                    # =====================================================

                    dbc.Checklist(

                        id="slow-only",

                        options=[

                            {

                                "label": "Show Slow Executions Only",

                                "value": 1

                            }

                        ],

                        value=[],

                        switch=True

                    ),

                    html.Br(),

                    dbc.Checklist(

                        id="critical-only",

                        options=[

                            {

                                "label": "Critical Failures Only",

                                "value": 1

                            }

                        ],

                        value=[],

                        switch=True

                    ),

                    html.Br(),

                    # =====================================================
                    # Buttons
                    # =====================================================

                    dbc.Button(

                        [

                            html.I(

                                className="bi bi-arrow-clockwise me-2"

                            ),

                            "Reset Filters"

                        ],

                        id="reset-filters",

                        color="secondary",

                        className="w-100 mb-2"

                    ),

                    dbc.Button(

                        [

                            html.I(

                                className="bi bi-download me-2"

                            ),

                            "Export Current View"

                        ],

                        id="export-view",

                        color="primary",

                        className="w-100"

                    )

                ]

            )

        ],

        className="sidebar-card shadow-sm"

    )