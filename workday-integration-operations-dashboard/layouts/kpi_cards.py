"""
Enterprise KPI Cards
"""

from dash import html
import dash_bootstrap_components as dbc


def build_kpi_card(

    title,
    value_id,
    icon,
    color,
    arrow_id=None

):

    return dbc.Card(

        dbc.CardBody(

            [

                dbc.Row(

                    [

                        dbc.Col(

                            [

                                html.Div(

                                    title,

                                    className="kpi-title"

                                ),

                                html.H2(

                                    "0",

                                    id=value_id,

                                    className="kpi-value",

                                    **{

                                        "data-value": 0

                                    }

                                )

                            ]

                        ),

                        dbc.Col(

                            html.Div(

                                html.I(

                                    className=icon

                                ),

                                className=f"kpi-icon icon-{color}"

                            ),

                            width="auto"

                        )

                    ],

                    align="center"

                ),

                html.Hr(),

                dbc.Row(

                    [

                        dbc.Col(

                            html.Small(

                                "Trend",

                                className="text-muted"

                            )

                        ),

                        dbc.Col(

                            html.H5(

                                "►",

                                id=arrow_id,

                                className="kpi-trend trend-neutral"

                            )

                            if arrow_id

                            else

                            html.Div(),

                            width="auto"

                        )

                    ],

                    align="center"

                )

            ]

        ),

        className=f"kpi-card card-{color}"

    )


def build_kpi_cards():

    cards = [

        (

            "Total Executions",

            "kpi-total-executions",

            "fa-solid fa-list-check",

            "primary",

            None

        ),

        (

            "Successful Executions",

            "kpi-successful-executions",

            "fa-solid fa-circle-check",

            "success",

            "kpi-success-arrow"

        ),

        (

            "Failed Executions",

            "kpi-failed-executions",

            "fa-solid fa-circle-xmark",

            "danger",

            "kpi-failure-arrow"

        ),

        (

            "Warning Executions",

            "kpi-warning-executions",

            "fa-solid fa-triangle-exclamation",

            "warning",

            None

        ),

        (

            "Success Rate",

            "kpi-success-rate",

            "fa-solid fa-chart-line",

            "success",

            None

        ),

        (

            "Failure Rate",

            "kpi-failure-rate",

            "fa-solid fa-chart-column",

            "danger",

            None

        ),

        (

            "Average Runtime",

            "kpi-average-runtime",

            "fa-solid fa-stopwatch",

            "primary",

            "kpi-runtime-arrow"

        ),

        (

            "Longest Runtime",

            "kpi-longest-runtime",

            "fa-solid fa-hourglass-end",

            "warning",

            None

        ),

        (

            "Active Integrations",

            "kpi-active-integrations",

            "fa-solid fa-plug",

            "primary",

            None

        ),

        (

            "Items Processed",

            "kpi-total-items",

            "fa-solid fa-boxes-stacked",

            "success",

            None

        ),

        (

            "Critical Failures",

            "kpi-critical-failures",

            "fa-solid fa-bug",

            "danger",

            None

        ),

        (

            "Processing Reports",

            "kpi-processing-reports",

            "fa-solid fa-file-lines",

            "primary",

            None

        ),

        (

            "Slow Integrations",

            "kpi-slow-integrations",

            "fa-solid fa-gauge-high",

            "warning",

            None

        ),

        (

            "Average Throughput",

            "kpi-throughput",

            "fa-solid fa-arrow-trend-up",

            "success",

            None

        ),

        (

            "Today's Executions",

            "kpi-today-executions",

            "fa-solid fa-calendar-day",

            "primary",

            None

        )

    ]

    return dbc.Row(

        [

            dbc.Col(

                build_kpi_card(

                    *card

                ),

                xl=3,

                lg=4,

                md=6,

                sm=12,

                className="mb-4"

            )

            for card in cards

        ],

        className="g-3"

    )