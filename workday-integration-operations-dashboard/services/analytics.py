"""
Enterprise Analytics Engine
"""

import pandas as pd
import numpy as np

from services.cache_manager import cached


class Analytics:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    # ======================================================
    # BASIC KPIs
    # ======================================================

    @cached()
    def total_executions(self):
        return len(self.df)

    @cached()
    def successful_executions(self):
        return (self.df["status"] == "Success").sum()

    @cached()
    def failed_executions(self):
        return (self.df["status"] == "Failed").sum()

    @cached()
    def warning_executions(self):
        return (self.df["status"] == "Warning").sum()

    @cached()
    def success_rate(self):

        if len(self.df) == 0:
            return 0

        return round(
            self.successful_executions() /
            len(self.df) * 100,
            2
        )

    @cached()
    def failure_rate(self):

        if len(self.df) == 0:
            return 0

        return round(
            self.failed_executions() /
            len(self.df) * 100,
            2
        )

    @cached()
    def average_processing_time(self):

        return round(

            self.df["processing_time_seconds"]

            .mean(),

            2

        )

    @cached()
    def longest_processing_time(self):

        return round(

            self.df["processing_time_seconds"]

            .max(),

            2

        )

    @cached()
    def active_integrations(self):

        return self.df["integration_system"].nunique()

    @cached()
    def total_items_processed(self):

        return int(

            self.df["items_processed"]

            .sum()

        )

    @cached()
    def slow_integrations(self):

        return int(

            (

                self.df["processing_time_seconds"]

                >= 30

            ).sum()

        )

    @cached()
    def todays_executions(self):

        today = pd.Timestamp.today().date()

        return int(

            (

                self.df["event_date"]

                .dt.date == today

            ).sum()

        )

    # ======================================================
    # EXECUTION TREND
    # ======================================================

    @cached()
    def execution_trend(self):

        return (

            self.df

            .groupby(

                self.df["event_date"].dt.date

            )

            .size()

            .reset_index(name="executions")

        )

    # ======================================================
    # STATUS DISTRIBUTION
    # ======================================================

    @cached()
    def status_distribution(self):

        return (

            self.df

            .groupby("status")

            .size()

            .reset_index(name="count")

            .sort_values(

                "count",

                ascending=False

            )

        )

    # ======================================================
    # TOP INTEGRATIONS
    # ======================================================

    @cached()
    def top_integrations(self, limit=10):

        return (

            self.df

            .groupby("integration_system")

            .size()

            .reset_index(name="executions")

            .sort_values(

                "executions",

                ascending=False

            )

            .head(limit)

        )

    # ======================================================
    # SLOWEST INTEGRATIONS
    # ======================================================

    @cached()
    def slowest_integrations(self, limit=10):

        return (

            self.df

            .groupby("integration_system")[

                "processing_time_seconds"

            ]

            .mean()

            .reset_index()

            .sort_values(

                "processing_time_seconds",

                ascending=False

            )

            .head(limit)

        )

    # ======================================================
    # FAILURE REASONS
    # ======================================================

    @cached()
    def failure_reasons(self, limit=20):

        if "errors_warnings" not in self.df.columns:

            return pd.DataFrame()

        failures = self.df[

            self.df["status"] == "Failed"

        ]

        return (

            failures

            .groupby("errors_warnings")

            .size()

            .reset_index(name="count")

            .sort_values(

                "count",

                ascending=False

            )

            .head(limit)

        )

    # ======================================================
    # WEEKDAY HEATMAP
    # ======================================================

    @cached()
    def weekday_heatmap(self):

        return pd.pivot_table(

            self.df,

            values="integration_system",

            index="day",

            columns="hour",

            aggfunc="count",

            fill_value=0

        )

    # ======================================================
    # HEALTH SCORE
    # ======================================================

    @cached()
    def integration_health(self):

        grouped = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("status", "count"),

                failures=("is_failed", "sum"),

                avg_runtime=("processing_time_seconds", "mean")

            )

            .reset_index()

        )

        grouped["health_score"] = (

            100

            -

            (

                grouped["failures"] * 5

            )

            -

            (

                grouped["avg_runtime"] / 5

            )

        )

        grouped["health_score"] = (

            grouped["health_score"]

            .clip(

                lower=0,

                upper=100

            )

            .round(2)

        )

        return grouped

    # ======================================================
    # TREND RANKING
    # ======================================================

    @cached()
    def trend_ranking(self):

        failures = self.df[

            self.df["status"] == "Failed"

        ].copy()

        failures["date"] = failures["event_date"].dt.date

        latest = failures["date"].max()

        previous = latest - pd.Timedelta(days=1)

        today = (

            failures[

                failures["date"] == latest

            ]

            .groupby("integration_system")

            .size()

        )

        yesterday = (

            failures[

                failures["date"] == previous

            ]

            .groupby("integration_system")

            .size()

        )

        trend = pd.concat(

            [

                today,

                yesterday

            ],

            axis=1

        ).fillna(0)

        trend.columns = [

            "today",

            "yesterday"

        ]

        trend["change"] = (

            trend["today"]

            -

            trend["yesterday"]

        )

        trend["trend"] = np.where(

            trend["change"] > 0,

            "▲ Worse",

            np.where(

                trend["change"] < 0,

                "▼ Improved",

                "▬ Stable"

            )

        )

        return (

            trend

            .reset_index()

            .sort_values(

                "change",

                ascending=False

            )

        )

    # ======================================================
    # MASTER KPI
    # ======================================================

    @cached()
    def dashboard_summary(self):

        return {

            "total_executions": self.total_executions(),

            "successful_executions": self.successful_executions(),

            "failed_executions": self.failed_executions(),

            "warning_executions": self.warning_executions(),

            "success_rate": self.success_rate(),

            "failure_rate": self.failure_rate(),

            "average_processing_time": self.average_processing_time(),

            "longest_processing_time": self.longest_processing_time(),

            "active_integrations": self.active_integrations(),

            "items_processed": self.total_items_processed(),

            "slow_integrations": self.slow_integrations(),

            "todays_executions": self.todays_executions()

        }