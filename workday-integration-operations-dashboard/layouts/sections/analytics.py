"""
Analytics Dashboard Section
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts.integration_health import IntegrationHealthChart
from charts.health_gauge import HealthGaugeChart
from charts.execution_waterfall import ExecutionWaterfallChart
from charts.items_treemap import ItemsTreemapChart
from charts.success_failure import SuccessFailureChart
from charts.integration_ranking import IntegrationRankingChart


class AnalyticsSection:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        health = IntegrationHealthChart(

            self.df

        ).build()

        gauges = HealthGaugeChart(

            self.df

        ).build()

        waterfall = ExecutionWaterfallChart(

            self.df

        ).build()

        items = ItemsTreemapChart(

            self.df

        ).build()

        success_failure = SuccessFailureChart(

            self.df

        ).build()

        ranking = IntegrationRankingChart(

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

                                        "Integration Health Matrix"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="integration-health",

                                            figure=health,

                                            config=IntegrationHealthChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=8

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Health Gauges"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="health-gauges",

                                            figure=gauges,

                                            config=HealthGaugeChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=4

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

                                        "Execution Waterfall"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="execution-waterfall",

                                            figure=waterfall,

                                            config=ExecutionWaterfallChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=5

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Items Processed"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="items-treemap",

                                            figure=items,

                                            config=ItemsTreemapChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=7

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

                                        "Success vs Failure"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="success-failure",

                                            figure=success_failure,

                                            config=SuccessFailureChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=7

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Integration Ranking"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="integration-ranking",

                                            figure=ranking,

                                            config=IntegrationRankingChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=5

                        )

                    ],

                    className="g-4"

                )

            ]

        )