"""
Performance Dashboard Section
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts.weekly_area import WeeklyAreaChart
from charts.monthly_area import MonthlyAreaChart
from charts.top_integrations import TopIntegrationsChart
from charts.slow_integrations import SlowIntegrationsChart
from charts.runtime_distribution import RuntimeDistributionChart
from charts.runtime_outliers import RuntimeOutliersChart
from charts.processing_timeline import ProcessingTimelineChart


class PerformanceSection:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        weekly = WeeklyAreaChart(

            self.df

        ).build()

        monthly = MonthlyAreaChart(

            self.df

        ).build()

        top = TopIntegrationsChart(

            self.df

        ).build()

        slow = SlowIntegrationsChart(

            self.df

        ).build()

        runtime_distribution = RuntimeDistributionChart(

            self.df

        ).build()

        runtime_outliers = RuntimeOutliersChart(

            self.df

        ).build()

        timeline = ProcessingTimelineChart(

            self.df

        ).build()

        return html.Div(

            [

                dbc.Row(

                    [

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Weekly Trend"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="weekly-area",

                                            figure=weekly,

                                            # config=WeeklyAreaChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Monthly Trend"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="monthly-area",

                                            figure=monthly,

                                            # config=MonthlyAreaChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        )

                    ],

                    className="g-4 mb-4"

                ),

                dbc.Row(

                    [

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Top Integrations"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="top-integrations",

                                            figure=top,

                                            # config=TopIntegrationsChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Slow Integrations"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="slow-integrations",

                                            figure=slow,

                                            # config=SlowIntegrationsChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        )

                    ],

                    className="g-4 mb-4"

                ),

                dbc.Row(

                    [

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Runtime Distribution"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="runtime-distribution",

                                            figure=runtime_distribution,

                                            # config=RuntimeDistributionChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Runtime Outliers"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="runtime-outliers",

                                            figure=runtime_outliers,

                                            # config=RuntimeOutliersChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6

                        )

                    ],

                    className="g-4 mb-4"

                ),

                dbc.Row(

                    [

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Processing Timeline"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="processing-timeline",

                                            figure=timeline,

                                            # config=ProcessingTimelineChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            width=12

                        )

                    ]

                )

            ]

        )