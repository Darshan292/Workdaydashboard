"""
Chart Callbacks
Updates every dashboard visualization
"""

import pandas as pd

from dash import Input
from dash import Output
from dash import callback

# ------------------------------------------------------------
# Overview
# ------------------------------------------------------------

from charts.execution_trend import ExecutionTrendChart
from charts.status_distribution import StatusDistributionChart
from charts.calendar_heatmap import CalendarHeatmapChart
from charts.weekday_heatmap import WeekdayHeatmapChart
from charts.hourly_trend import HourlyTrendChart

# ------------------------------------------------------------
# Performance
# ------------------------------------------------------------

from charts.weekly_area import WeeklyAreaChart
from charts.monthly_area import MonthlyAreaChart
from charts.top_integrations import TopIntegrationsChart
from charts.slow_integrations import SlowIntegrationsChart
from charts.runtime_distribution import RuntimeDistributionChart
from charts.runtime_outliers import RuntimeOutliersChart
from charts.processing_timeline import ProcessingTimelineChart

# ------------------------------------------------------------
# Failures
# ------------------------------------------------------------

from charts.failure_trend import FailureTrendChart
from charts.failure_treemap import FailureTreemapChart
from charts.failure_sunburst import FailureSunburstChart
from charts.failure_sankey import FailureSankeyChart
from charts.error_wordcloud import ErrorWordCloudChart

# ------------------------------------------------------------
# Analytics
# ------------------------------------------------------------

from charts.integration_health import IntegrationHealthChart
from charts.health_gauge import HealthGaugeChart
from charts.execution_waterfall import ExecutionWaterfallChart
from charts.items_treemap import ItemsTreemapChart
from charts.processing_violin import ProcessingViolinChart
from charts.success_failure import SuccessFailureChart
from charts.integration_ranking import IntegrationRankingChart

# ------------------------------------------------------------
# Monitoring
# ------------------------------------------------------------

from charts.execution_timeline import ExecutionTimelineChart
from charts.trend_ranking import TrendRankingChart


def register_chart_callbacks(app):

    @app.callback(

        [

            # ==================================================
            # Overview
            # ==================================================

            Output(
                "execution-trend",
                "figure"
            ),

            Output(
                "status-distribution",
                "figure"
            ),

            Output(
                "calendar-heatmap",
                "figure"
            ),

            Output(
                "weekday-heatmap",
                "figure"
            ),

            Output(
                "hourly-trend",
                "figure"
            ),

            # ==================================================
            # Performance
            # ==================================================

            Output(
                "weekly-area",
                "figure"
            ),

            Output(
                "monthly-area",
                "figure"
            ),

            Output(
                "top-integrations",
                "figure"
            ),

            Output(
                "slow-integrations",
                "figure"
            ),

            Output(
                "runtime-distribution",
                "figure"
            ),

            Output(
                "runtime-outliers",
                "figure"
            ),

            Output(
                "processing-timeline",
                "figure"
            ),

            # ==================================================
            # Failures
            # ==================================================

            Output(
                "failure-trend",
                "figure"
            ),

            Output(
                "failure-treemap",
                "figure"
            ),

            Output(
                "failure-sunburst",
                "figure"
            ),

            Output(
                "failure-sankey",
                "figure"
            ),

            Output(
                "error-wordcloud",
                "figure"
            ),

            # ==================================================
            # Analytics
            # ==================================================

            Output(
                "integration-health",
                "figure"
            ),

            Output(
                "health-gauges",
                "figure"
            ),

            Output(
                "execution-waterfall",
                "figure"
            ),

            Output(
                "items-treemap",
                "figure"
            ),

            Output(
                "processing-violin",
                "figure"
            ),

            Output(
                "success-failure",
                "figure"
            ),

            Output(
                "integration-ranking",
                "figure"
            ),

            # ==================================================
            # Monitoring
            # ==================================================

            Output(
                "execution-timeline",
                "figure"
            ),

            Output(
                "trend-ranking",
                "figure"
            )

        ],

        Input(

            "filtered-data",

            "data"

        )

    )

    def update_all_charts(

        filtered_data

    ):

        if filtered_data is None:

            df = pd.DataFrame()

        else:

            df = pd.DataFrame(

                filtered_data

            )

        if not df.empty:

            if "event_date" in df.columns:

                df["event_date"] = pd.to_datetime(

                    df["event_date"],

                    errors="coerce"

                )

        # =====================================================
        # Chart Generation Starts Here
        # =====================================================

        # =====================================================
        # Overview Charts
        # =====================================================
        import time

        start = time.perf_counter()

        execution_trend = (

            ExecutionTrendChart(

                df

            )

            .build()

        )
        print(f"ExecutionTrend: {time.perf_counter() - start:.2f}s")

        status_distribution = (

            StatusDistributionChart(

                df

            )

            .build()

        )
        print(f"StatustDistribution: {time.perf_counter() - start:.2f}s")


        calendar_heatmap = (

            CalendarHeatmapChart(

                df

            )

            .build()

        )
        print(f"CalenderHeatmap: {time.perf_counter() - start:.2f}s")


        weekday_heatmap = (

            WeekdayHeatmapChart(

                df

            )

            .build()

        )
        print(f"WeekdayHeatmap: {time.perf_counter() - start:.2f}s")


        hourly_trend = (

            HourlyTrendChart(

                df

            )

            .build()

        )
        print(f"HourlyHeatmap: {time.perf_counter() - start:.2f}s")


        # =====================================================
        # Performance Charts
        # =====================================================

        weekly_area = (

            WeeklyAreaChart(

                df

            )

            .build()

        )
        print(f"weeklyare: {time.perf_counter() - start:.2f}s")


        monthly_area = (

            MonthlyAreaChart(

                df

            )

            .build()

        )
        print(f"Monthlyare: {time.perf_counter() - start:.2f}s")


        top_integrations = (

            TopIntegrationsChart(

                df

            )

            .build()

        )
        print(f"topintegrations: {time.perf_counter() - start:.2f}s")


        slow_integrations = (

            SlowIntegrationsChart(

                df

            )

            .build()

        )
        print(f"slowintegrations: {time.perf_counter() - start:.2f}s")


        runtime_distribution = (

            RuntimeDistributionChart(

                df

            )

            .build()

        )
        print(f"runtimedistribution: {time.perf_counter() - start:.2f}s")


        runtime_outliers = (

            RuntimeOutliersChart(

                df

            )

            .build()

        )
        print(f"runtimeoutliers: {time.perf_counter() - start:.2f}s")


        processing_timeline = (

            ProcessingTimelineChart(

                df

            )

            .build()

        )
        print(f"processingtimeline: {time.perf_counter() - start:.2f}s")


        # =====================================================
        # Prepare Return Objects (Part 1)
        # =====================================================

        figures = [

            # ---------------------------------------------
            # Overview
            # ---------------------------------------------

            execution_trend,

            status_distribution,

            calendar_heatmap,

            weekday_heatmap,

            hourly_trend,

            # ---------------------------------------------
            # Performance
            # ---------------------------------------------

            weekly_area,

            monthly_area,

            top_integrations,

            slow_integrations,

            runtime_distribution,

            runtime_outliers,

            processing_timeline

        ]

        # =====================================================
        # Continue in Part 3
        # =====================================================

                # =====================================================
        # Failure Analytics
        # =====================================================

        failure_trend = (

            FailureTrendChart(

                df

            ).build()

        )
        print(f"failuretrend: {time.perf_counter() - start:.2f}s")


        failure_treemap = (

            FailureTreemapChart(

                df

            ).build()

        )
        print(f"failuretreemap: {time.perf_counter() - start:.2f}s")


        failure_sunburst = (

            FailureSunburstChart(

                df

            ).build()

        )
        print(f"failuresunburts: {time.perf_counter() - start:.2f}s")


        failure_sankey = (

            FailureSankeyChart(

                df

            ).build()

        )
        print(f"failuresankey: {time.perf_counter() - start:.2f}s")


        error_wordcloud = (

            ErrorWordCloudChart(

                df

            ).build()

        )
        print(f"errorwordcloud: {time.perf_counter() - start:.2f}s")


        # =====================================================
        # Analytics
        # =====================================================

        integration_health = (

            IntegrationHealthChart(

                df

            ).build()

        )
        print(f"integrationhealth: {time.perf_counter() - start:.2f}s")


        health_gauges = (

            HealthGaugeChart(

                df

            ).build()

        )
        print(f"healthgauges: {time.perf_counter() - start:.2f}s")


        execution_waterfall = (

            ExecutionWaterfallChart(

                df

            ).build()

        )
        print(f"executionwaterfall: {time.perf_counter() - start:.2f}s")


        items_treemap = (

            ItemsTreemapChart(

                df

            ).build()

        )
        print(f"itemstreemap: {time.perf_counter() - start:.2f}s")


        processing_violin = (

            ProcessingViolinChart(

                df

            ).build()

        )
        print(f"processingviolin: {time.perf_counter() - start:.2f}s")


        success_failure = (

            SuccessFailureChart(

                df

            ).build()

        )
        print(f"successfailure: {time.perf_counter() - start:.2f}s")


        integration_ranking = (

            IntegrationRankingChart(

                df

            ).build()

        )
        print(f"integrationranking: {time.perf_counter() - start:.2f}s")


        # =====================================================
        # Extend Figure List
        # =====================================================

        figures.extend(

            [

                # -----------------------------------------
                # Failure Analytics
                # -----------------------------------------

                failure_trend,

                failure_treemap,

                failure_sunburst,

                failure_sankey,

                error_wordcloud,

                # -----------------------------------------
                # Analytics
                # -----------------------------------------

                integration_health,

                health_gauges,

                execution_waterfall,

                items_treemap,

                processing_violin,

                success_failure,

                integration_ranking

            ]

        )

        # =====================================================
        # Continue in Part 4
        # =====================================================

                # =====================================================
        # Monitoring
        # =====================================================

        execution_timeline = (

            ExecutionTimelineChart(

                df

            ).build()

        )
        print(f"ExecutionTimeline: {time.perf_counter() - start:.2f}s")


        trend_ranking = (

            TrendRankingChart(

                df

            ).build()

        )
        print(f"trendranking: {time.perf_counter() - start:.2f}s")


        # =====================================================
        # Append Monitoring Charts
        # =====================================================

        figures.extend(

            [

                execution_timeline,

                trend_ranking

            ]

        )

        # =====================================================
        # Safety Check
        # =====================================================

        expected_outputs = 26

        if len(figures) != expected_outputs:

            raise ValueError(

                f"Expected {expected_outputs} chart outputs "

                f"but generated {len(figures)}."

            )

        # =====================================================
        # Return All Figures
        # =====================================================

        return tuple(

            figures

        )

