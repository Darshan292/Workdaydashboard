"""
Enterprise KPI Engine
"""

import pandas as pd
import numpy as np


class KPIEngine:

    def __init__(self, df):

        self.df = df.copy()

        # Convert event_date back to datetime
        if "event_date" in self.df.columns:
            self.df["event_date"] = pd.to_datetime(
                self.df["event_date"],
                errors="coerce"
            )

        # Convert numeric columns
        numeric_columns = [
            "processing_time_seconds",
            "items_processed"
        ]

        for column in numeric_columns:
            if column in self.df.columns:
                self.df[column] = pd.to_numeric(
                    self.df[column],
                    errors="coerce"
                )

    # ======================================================
    # Helpers
    # ======================================================

    def _current_previous(self):

        if self.df.empty or "event_date" not in self.df.columns:
            return pd.DataFrame(), pd.DataFrame()

        valid_dates = self.df["event_date"].dropna()

        if valid_dates.empty:
            return pd.DataFrame(), pd.DataFrame()

        latest = valid_dates.dt.date.max()
        previous = latest - pd.Timedelta(days=1)

        current = self.df[
            self.df["event_date"].dt.date == latest
        ]

        previous_df = self.df[
            self.df["event_date"].dt.date == previous
        ]

        return current, previous_df

    def _delta(self, current, previous):

        change = current - previous

        if change > 0:
            arrow = "▲"

        elif change < 0:
            arrow = "▼"

        else:
            arrow = "▬"

        percent = 0

        if previous != 0:
            percent = round(change / previous * 100, 2)

        return {
            "current": current,
            "previous": previous,
            "change": change,
            "percent": percent,
            "arrow": arrow
        }

    # ======================================================
    # KPI Calculations
    # ======================================================

    def total_executions(self):

        current, previous = self._current_previous()

        return self._delta(

            len(current),

            len(previous)

        )

    def successful_executions(self):

        current, previous = self._current_previous()

        return self._delta(

            (current["status"] == "Success").sum(),

            (previous["status"] == "Success").sum()

        )

    def failed_executions(self):

        current, previous = self._current_previous()

        return self._delta(

            (current["status"] == "Failed").sum(),

            (previous["status"] == "Failed").sum()

        )

    def warning_executions(self):

        current, previous = self._current_previous()

        return self._delta(

            (current["status"] == "Warning").sum(),

            (previous["status"] == "Warning").sum()

        )

    def success_rate(self):

        current, previous = self._current_previous()

        current_rate = 0
        previous_rate = 0

        if len(current):

            current_rate = round(

                (current["status"] == "Success").sum()

                / len(current)

                * 100,

                2

            )

        if len(previous):

            previous_rate = round(

                (previous["status"] == "Success").sum()

                / len(previous)

                * 100,

                2

            )

        return self._delta(

            current_rate,

            previous_rate

        )

    def failure_rate(self):

        current, previous = self._current_previous()

        current_rate = 0
        previous_rate = 0

        if len(current):

            current_rate = round(

                (current["status"] == "Failed").sum()

                / len(current)

                * 100,

                2

            )

        if len(previous):

            previous_rate = round(

                (previous["status"] == "Failed").sum()

                / len(previous)

                * 100,

                2

            )

        return self._delta(

            current_rate,

            previous_rate

        )

    def average_processing_time(self):

        current, previous = self._current_previous()

        return self._delta(

            round(
                current["processing_time_seconds"].mean(),
                2
            ),

            round(
                previous["processing_time_seconds"].mean(),
                2
            )

        )

    def longest_processing_time(self):

        return {

            "value": round(

                self.df["processing_time_seconds"].max(),

                2

            )

        }

    def active_integrations(self):

        return {

            "value":

            self.df["integration_system"].nunique()

        }

    def total_items_processed(self):

        return {

            "value":

            int(

                self.df["items_processed"].sum()

            )

        }

    def slow_integrations(self):

        return {

            "value":

            int(

                (

                    self.df["processing_time_seconds"]

                    >= 30

                ).sum()

            )

        }

    def critical_failures(self):

        return {

            "value":

            int(

                (

                    self.df["status"]

                    == "Failed"

                ).sum()

            )

        }

    def average_throughput(self):

        runtime = self.df["processing_time_seconds"].replace(

            0,

            np.nan

        )

        throughput = (

            self.df["items_processed"]

            / runtime

        )

        return {

            "value":

            round(

                throughput.mean(),

                2

            )

        }

    def todays_executions(self):

        current, _ = self._current_previous()

        return {

            "value":

            len(current)

        }

    # ======================================================
    # Dashboard KPI Dictionary
    # ======================================================

    def build(self):

        return {

            "total_executions":

                self.total_executions(),

            "successful_executions":

                self.successful_executions(),

            "failed_executions":

                self.failed_executions(),

            "warning_executions":

                self.warning_executions(),

            "success_rate":

                self.success_rate(),

            "failure_rate":

                self.failure_rate(),

            "average_processing_time":

                self.average_processing_time(),

            "longest_processing_time":

                self.longest_processing_time(),

            "active_integrations":

                self.active_integrations(),

            "items_processed":

                self.total_items_processed(),

            "critical_failures":

                self.critical_failures(),

            "slow_integrations":

                self.slow_integrations(),

            "average_throughput":

                self.average_throughput(),

            "todays_executions":

                self.todays_executions()

        }


if __name__ == "__main__":

    from services.excel_parser import ExcelParser
    from services.data_cleaner import DataCleaner
    from services.data_merger import DataMerger

    parser = ExcelParser()

    frames = parser.load_all()

    cleaned = {}

    for k, v in frames.items():

        cleaned[k] = DataCleaner(v).clean()

    master = DataMerger(cleaned).merge()

    engine = KPIEngine(master)

    from pprint import pprint

    pprint(engine.build())