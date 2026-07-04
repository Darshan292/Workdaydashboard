"""
Failure Analytics Section
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts.failure_trend import FailureTrendChart
from charts.failure_treemap import FailureTreemapChart
from charts.failure_sunburst import FailureSunburstChart
from charts.failure_sankey import FailureSankeyChart
from charts.error_wordcloud import ErrorWordCloudChart


class FailureSection:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        failure_trend = FailureTrendChart(

            self.df

        ).build()

        treemap = FailureTreemapChart(

            self.df

        ).build()

        sunburst = FailureSunburstChart(

            self.df

        ).build()

        sankey = FailureSankeyChart(

            self.df

        ).build()

        wordcloud = ErrorWordCloudChart(

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

                                        "Failure Trend"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="failure-trend",

                                            figure=failure_trend,

                                            config=FailureTrendChart.config()

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=12

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

                                        "Failure Treemap"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="failure-treemap",

                                            figure=treemap,

                                            config=FailureTreemapChart.config()

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

                                        "Failure Sunburst"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="failure-sunburst",

                                            figure=sunburst,

                                            config=FailureSunburstChart.config()

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

                                        "Failure Flow"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="failure-sankey",

                                            figure=sankey,

                                            config=FailureSankeyChart.config()

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

                                        "Error Keyword Analysis"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="error-wordcloud",

                                            figure=wordcloud,

                                            config=ErrorWordCloudChart.config()

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