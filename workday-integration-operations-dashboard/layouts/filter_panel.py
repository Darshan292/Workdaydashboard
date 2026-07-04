"""
Reusable Filter Panel Components
"""

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc


class FilterPanel:

    @staticmethod
    def search():

        return html.Div(

            [

                html.Label(

                    "Search Integration",

                    className="filter-label"

                ),

                dbc.Input(

                    id="search-integration",

                    placeholder="Search Integration..."

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

        )

    @staticmethod
    def period():

        return html.Div(

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

        )

    @staticmethod
    def integration():

        return html.Div(

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

        )

    @staticmethod
    def status():

        return html.Div(

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

        )

    @staticmethod
    def processing():

        return html.Div(

            [

                html.Label(

                    "Processing Time",

                    className="filter-label"

                ),

                dcc.RangeSlider(

                    id="processing-slider",

                    min=0,

                    max=300,

                    value=[

                        0,

                        300

                    ]

                )

            ],

            className="filter-group"

        )

    @staticmethod
    def items():

        return html.Div(

            [

                html.Label(

                    "Items Processed",

                    className="filter-label"

                ),

                dcc.RangeSlider(

                    id="items-slider",

                    min=0,

                    max=100000,

                    value=[

                        0,

                        100000

                    ]

                )

            ],

            className="filter-group"

        )

    @staticmethod
    def failure():

        return html.Div(

            [

                html.Label(

                    "Failure Reason",

                    className="filter-label"

                ),

                dbc.Input(

                    id="failure-filter"

                )

            ],

            className="filter-group"

        )

    @staticmethod
    def report():

        return html.Div(

            [

                html.Label(

                    "Report Type",

                    className="filter-label"

                ),

                dcc.Dropdown(

                    id="report-filter"

                )

            ],

            className="filter-group"

        )

    @staticmethod
    def reset_button():

        return dbc.Button(

            "Reset Filters",

            id="reset-filters",

            color="danger",

            className="w-100"

        )