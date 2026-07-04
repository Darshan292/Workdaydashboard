"""
Enterprise Dashboard Chart Grid
"""

from dash import html
import dash_bootstrap_components as dbc

from layouts.sections.overview import OverviewSection
from layouts.sections.performance import PerformanceSection
from layouts.sections.failures import FailureSection
from layouts.sections.analytics import AnalyticsSection
from layouts.sections.monitoring import MonitoringSection


class ChartGrid:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        return dbc.Container(

            [

                # =====================================================
                # OVERVIEW
                # =====================================================

                html.Div(

                    [

                        html.H3(

                            "Overview",

                            className="section-title"

                        ),

                        html.Hr(

                            className="section-divider"

                        ),

                        OverviewSection(

                            self.df

                        ).build()

                    ],

                    id="overview-section",

                    className="dashboard-section fade-section"

                ),

                # =====================================================
                # PERFORMANCE
                # =====================================================

                html.Div(

                    [

                        html.H3(

                            "Performance Analytics",

                            className="section-title"

                        ),

                        html.Hr(

                            className="section-divider"

                        ),

                        PerformanceSection(

                            self.df

                        ).build()

                    ],

                    id="performance-section",

                    className="dashboard-section fade-section"

                ),

                # =====================================================
                # FAILURES
                # =====================================================

                html.Div(

                    [

                        html.H3(

                            "Failure Analytics",

                            className="section-title"

                        ),

                        html.Hr(

                            className="section-divider"

                        ),

                        FailureSection(

                            self.df

                        ).build()

                    ],

                    id="failure-section",

                    className="dashboard-section fade-section"

                ),

                # =====================================================
                # HEALTH & ANALYTICS
                # =====================================================

                html.Div(

                    [

                        html.H3(

                            "Integration Health",

                            className="section-title"

                        ),

                        html.Hr(

                            className="section-divider"

                        ),

                        AnalyticsSection(

                            self.df

                        ).build()

                    ],

                    id="analytics-section",

                    className="dashboard-section fade-section"

                ),

                # =====================================================
                # MONITORING
                # =====================================================

                html.Div(

                    [

                        html.H3(

                            "Operations Monitoring",

                            className="section-title"

                        ),

                        html.Hr(

                            className="section-divider"

                        ),

                        MonitoringSection(

                            self.df

                        ).build()

                    ],

                    id="monitoring-section",

                    className="dashboard-section fade-section"

                )

            ],

            fluid=True,

            className="chart-grid-container"

        )