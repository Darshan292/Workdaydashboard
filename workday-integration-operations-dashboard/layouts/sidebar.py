"""
Enterprise Sidebar
"""

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def build_sidebar():

    return html.Div(

        id="sidebar",

        className="sidebar expanded",

        children=[

            # =====================================================
            # Header
            # =====================================================

            dbc.Row(

                [

                    dbc.Col(

                        html.H4(

                            "Filters",

                            className="sidebar-title"

                        )

                    ),

                    dbc.Col(

                        dbc.Button(

                            html.I(

                                className="fa-solid fa-bars"

                            ),

                            id="sidebar-toggle",

                            color="primary",

                            size="sm",

                            className="sidebar-toggle"

                        ),

                        width="auto"

                    )

                ],

                justify="between",

                align="center"

            ),

            html.Hr(className="sidebar-divider"),

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

                        placeholder="Search..."

                    ),

                    dbc.Button(

                        "Clear",

                        id="clear-search",

                        color="link",

                        size="sm",

                        className="mt-2"

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Period
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Period",

                        className="filter-label"

                    ),

                    dbc.Select(

                        id="period-filter",

                        value="weekly",

                        options=[

                            {

                                "label":"Daily",

                                "value":"daily"

                            },

                            {

                                "label":"Weekly",

                                "value":"weekly"

                            },

                            {

                                "label":"Monthly",

                                "value":"monthly"

                            }

                        ]

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Integration
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Integration",

                        className="filter-label"

                    ),

                    dcc.Dropdown(

                        id="integration-filter",

                        multi=True,

                        placeholder="All Integrations"

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Status
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Status",

                        className="filter-label"

                    ),

                    dcc.Dropdown(

                        id="status-filter",

                        multi=True,

                        placeholder="All Status"

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Runtime
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Processing Time (sec)",

                        className="filter-label"

                    ),

                    dcc.RangeSlider(

                        id="processing-slider",

                        min=0,

                        max=300,

                        value=[0,300],

                        tooltip={

                            "placement":"bottom"

                        }

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Items
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

                        value=[0,100000]

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Failure Reason
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Failure Reason",

                        className="filter-label"

                    ),

                    dbc.Input(

                        id="failure-filter",

                        placeholder="Timeout..."

                    )

                ],

                className="filter-group"

            ),

            # =====================================================
            # Report
            # =====================================================

            html.Div(

                [

                    html.Label(

                        "Report Type",

                        className="filter-label"

                    ),

                    dcc.Dropdown(

                        id="report-filter",

                        placeholder="Select Report"

                    )

                ],

                className="filter-group"

            ),

            html.Hr(className="sidebar-divider"),

            # =====================================================
            # Buttons
            # =====================================================

            dbc.Button(

                [

                    html.I(

                        className="fa-solid fa-arrow-rotate-left me-2"

                    ),

                    "Reset Filters"

                ],

                id="reset-filters",

                color="danger",

                className="w-100"

            ),

            html.Br(),

            html.Br(),

            dbc.Row(

                [

                    dbc.Col(

                        dbc.Badge(

                            "0 Active",

                            id="filter-badge",

                            color="primary"

                        )

                    ),

                    dbc.Col(

                        html.Div(

                            id="active-filter-count",

                            children="0 Active",

                            className="text-end"

                        )

                    )

                ]

            )

        ]

    )