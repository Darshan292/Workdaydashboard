"""
Monitoring Dashboard Section
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts.processing_violin import ProcessingViolinChart
from charts.execution_timeline import ExecutionTimelineChart
from charts.trend_ranking import TrendRankingChart
from charts.live_activity import LiveActivityFeed


class MonitoringSection:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        processing_violin = ProcessingViolinChart(

            self.df

        ).build()

        execution_timeline = ExecutionTimelineChart(

            self.df

        ).build()

        trend_ranking = TrendRankingChart(

            self.df

        ).build()

        live_feed = LiveActivityFeed(

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

                                        "Processing Time Distribution"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="processing-violin",

                                            figure=processing_violin,

                                            config=ProcessingViolinChart.config(),

                                            className="enterprise-chart"

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

                                        "Integration Trend Ranking"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="trend-ranking",

                                            figure=trend_ranking,

                                            config=TrendRankingChart.config(),

                                            className="enterprise-chart"

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

                                        "Execution Timeline"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="execution-timeline",

                                            figure=execution_timeline,

                                            config=ExecutionTimelineChart.config(),

                                            className="enterprise-chart"

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

                                        "Live Activity Feed"

                                    ),

                                    dbc.CardBody(

                                        live_feed

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=4

                        )

                    ],

                    className="g-4"

                )

            ]

        )