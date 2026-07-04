"""
Overview Dashboard Section
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

from charts.execution_trend import ExecutionTrendChart
from charts.status_distribution import StatusDistributionChart
from charts.calendar_heatmap import CalendarHeatmapChart
from charts.weekday_heatmap import WeekdayHeatmapChart
from charts.hourly_trend import HourlyTrendChart


class OverviewSection:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        execution_trend = ExecutionTrendChart(
            self.df
        ).build()

        status_distribution = StatusDistributionChart(
            self.df
        ).build()

        calendar_heatmap = CalendarHeatmapChart(
            self.df
        ).build()

        weekday_heatmap = WeekdayHeatmapChart(
            self.df
        ).build()

        hourly_trend = HourlyTrendChart(
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

                                        "Execution Trend"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(
                                            id="execution-trend",
                                            figure=execution_trend,
                                            className="enterprise-chart"
                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=8,

                            md=12

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Execution Status"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="status-distribution",

                                            figure=status_distribution,

                                            # config=StatusDistributionChart.config(),

                                            className="enterprise-chart"

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=4,

                            md=12

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

                                        "Execution Calendar"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="calendar-heatmap",

                                            figure=calendar_heatmap,

                                            # config=CalendarHeatmapChart.config(),

                                            className="enterprise-chart"

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6,

                            md=12

                        ),

                        dbc.Col(

                            dbc.Card(

                                [

                                    dbc.CardHeader(

                                        "Weekday Heatmap"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="weekday-heatmap",

                                            figure=weekday_heatmap,

                                            # config=WeekdayHeatmapChart.config(),

                                            className="enterprise-chart"

                                        )

                                    )

                                ],

                                className="dashboard-card"

                            ),

                            lg=6,

                            md=12

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

                                        "Hourly Execution Pattern"

                                    ),

                                    dbc.CardBody(

                                        dcc.Graph(

                                            id="hourly-trend",

                                            figure=hourly_trend,

                                            # config=HourlyTrendChart.config(),

                                            className="enterprise-chart"

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