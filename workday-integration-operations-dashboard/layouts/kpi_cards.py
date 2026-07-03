"""
Enterprise KPI Cards
"""

from dash import html
import dash_bootstrap_components as dbc


KPI_CONFIG = [

    {
        "id": "kpi-total",
        "title": "Total Executions",
        "icon": "bi bi-bar-chart-fill",
        "color": "primary"
    },

    {
        "id": "kpi-success",
        "title": "Successful",
        "icon": "bi bi-check-circle-fill",
        "color": "success"
    },

    {
        "id": "kpi-failed",
        "title": "Failed",
        "icon": "bi bi-x-circle-fill",
        "color": "danger"
    },

    {
        "id": "kpi-warning",
        "title": "Warnings",
        "icon": "bi bi-exclamation-triangle-fill",
        "color": "warning"
    },

    {
        "id": "kpi-success-rate",
        "title": "Success Rate",
        "icon": "bi bi-graph-up-arrow",
        "color": "success"
    },

    {
        "id": "kpi-failure-rate",
        "title": "Failure Rate",
        "icon": "bi bi-graph-down-arrow",
        "color": "danger"
    },

    {
        "id": "kpi-avg-runtime",
        "title": "Avg Runtime",
        "icon": "bi bi-clock-history",
        "color": "info"
    },

    {
        "id": "kpi-max-runtime",
        "title": "Max Runtime",
        "icon": "bi bi-stopwatch-fill",
        "color": "secondary"
    },

    {
        "id": "kpi-integrations",
        "title": "Active Integrations",
        "icon": "bi bi-diagram-3-fill",
        "color": "primary"
    },

    {
        "id": "kpi-items",
        "title": "Items Processed",
        "icon": "bi bi-box-seam-fill",
        "color": "primary"
    },

    {
        "id": "kpi-critical",
        "title": "Critical Failures",
        "icon": "bi bi-fire",
        "color": "danger"
    },

    {
        "id": "kpi-reports",
        "title": "Reports",
        "icon": "bi bi-file-earmark-bar-graph-fill",
        "color": "secondary"
    },

    {
        "id": "kpi-slow",
        "title": "Slow Integrations",
        "icon": "bi bi-hourglass-split",
        "color": "warning"
    },

    {
        "id": "kpi-throughput",
        "title": "Throughput",
        "icon": "bi bi-lightning-charge-fill",
        "color": "info"
    },

    {
        "id": "kpi-today",
        "title": "Today's Executions",
        "icon": "bi bi-calendar-event-fill",
        "color": "success"
    }

]


def create_kpi_card(card):

    return dbc.Col(

        dbc.Card(

            dbc.CardBody(

                [

                    html.Div(

                        [

                            html.Div(

                                [

                                    html.I(

                                        className=f"{card['icon']} kpi-icon"

                                    )

                                ],

                                className=f"kpi-icon-container bg-{card['color']}"

                            ),

                            html.Div(

                                [

                                    html.Div(

                                        card["title"],

                                        className="kpi-title"

                                    ),

                                    html.H2(

                                        "0",

                                        id=f"{card['id']}-value",

                                        className="kpi-value"

                                    ),

                                    html.Div(

                                        [

                                            html.Span(

                                                "▬",

                                                id=f"{card['id']}-arrow",

                                                className="kpi-arrow"

                                            ),

                                            html.Span(

                                                "0%",

                                                id=f"{card['id']}-delta",

                                                className="kpi-delta"

                                            )

                                        ],

                                        className="kpi-trend"

                                    )

                                ],

                                className="kpi-content"

                            )

                        ],

                        className="kpi-wrapper"

                    )

                ]

            ),

            className="kpi-card"

        ),

        xl=2,
        lg=3,
        md=4,
        sm=6,
        xs=12

    )


def create_kpi_section():

    rows = []

    current = []

    for index, card in enumerate(KPI_CONFIG):

        current.append(

            create_kpi_card(card)

        )

        if len(current) == 5:

            rows.append(

                dbc.Row(

                    current,

                    className="g-3 mb-3"

                )

            )

            current = []

    if current:

        rows.append(

            dbc.Row(

                current,

                className="g-3"

            )

        )

    return html.Div(

        rows,

        id="kpi-section"

    )