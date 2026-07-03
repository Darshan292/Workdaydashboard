"""
Enterprise Trend Engine
"""

import numpy as np
import pandas as pd


class TrendEngine:

    def __init__(self, df):

        self.df = df.copy()

        self.df["event_date"] = pd.to_datetime(
            self.df["event_date"],
            errors="coerce"
        )

    # =====================================================
    # Daily Execution Trend
    # =====================================================

    def daily_trend(self):

        trend = (

            self.df

            .groupby(

                self.df["event_date"].dt.date

            )

            .size()

            .reset_index(name="executions")

            .rename(columns={"event_date": "date"})

        )

        trend["moving_average"] = (

            trend["executions"]

            .rolling(3, min_periods=1)

            .mean()

            .round(2)

        )

        return trend

    # =====================================================
    # Weekly Trend
    # =====================================================

    def weekly_trend(self):

        trend = (

            self.df

            .groupby(

                self.df["event_date"]

                .dt.to_period("W")

            )

            .size()

            .reset_index(name="executions")

        )

        trend["week"] = trend["event_date"].astype(str)

        trend.drop(columns=["event_date"], inplace=True)

        return trend

    # =====================================================
    # Monthly Trend
    # =====================================================

    def monthly_trend(self):

        trend = (

            self.df

            .groupby(

                self.df["event_date"]

                .dt.to_period("M")

            )

            .size()

            .reset_index(name="executions")

        )

        trend["month"] = trend["event_date"].astype(str)

        trend.drop(columns=["event_date"], inplace=True)

        return trend

    # =====================================================
    # Failure Trend
    # =====================================================

    def failure_trend(self):

        failures = self.df[

            self.df["status"] == "Failed"

        ]

        return (

            failures

            .groupby(

                failures["event_date"].dt.date

            )

            .size()

            .reset_index(name="failures")

        )

    # =====================================================
    # Success Trend
    # =====================================================

    def success_trend(self):

        success = self.df[

            self.df["status"] == "Success"

        ]

        return (

            success

            .groupby(

                success["event_date"].dt.date

            )

            .size()

            .reset_index(name="success")

        )

    # =====================================================
    # Integration Trend
    # =====================================================

    def integration_trend(self):

        return (

            self.df

            .groupby(

                [

                    self.df["event_date"].dt.date,

                    "integration_system"

                ]

            )

            .size()

            .reset_index(name="executions")

        )

    # =====================================================
    # Trend Ranking
    # =====================================================

    def trend_ranking(self):

        failures = self.df[

            self.df["status"] == "Failed"

        ].copy()

        failures["date"] = failures["event_date"].dt.date

        dates = sorted(

            failures["date"]

            .dropna()

            .unique()

        )

        if len(dates) < 2:

            return pd.DataFrame()

        latest = dates[-1]

        previous = dates[-2]

        current = (

            failures[

                failures["date"] == latest

            ]

            .groupby("integration_system")

            .size()

        )

        prev = (

            failures[

                failures["date"] == previous

            ]

            .groupby("integration_system")

            .size()

        )

        trend = pd.concat(

            [

                current,

                prev

            ],

            axis=1

        ).fillna(0)

        trend.columns = [

            "current",

            "previous"

        ]

        trend["difference"] = (

            trend["current"]

            -

            trend["previous"]

        )

        trend["percentage"] = np.where(

            trend["previous"] == 0,

            100,

            round(

                trend["difference"]

                /

                trend["previous"]

                * 100,

                2

            )

        )

        trend["trend"] = np.select(

            [

                trend["difference"] > 0,

                trend["difference"] < 0

            ],

            [

                "⬆ Worse",

                "⬇ Improved"

            ],

            default="➡ Stable"

        )

        trend = (

            trend

            .reset_index()

            .sort_values(

                "difference",

                ascending=False

            )

        )

        return trend

    # =====================================================
    # Top Improved
    # =====================================================

    def most_improved(self, limit=10):

        ranking = self.trend_ranking()

        return (

            ranking

            .sort_values(

                "difference"

            )

            .head(limit)

        )

    # =====================================================
    # Most Degraded
    # =====================================================

    def most_degraded(self, limit=10):

        ranking = self.trend_ranking()

        return (

            ranking

            .sort_values(

                "difference",

                ascending=False

            )

            .head(limit)

        )

    # =====================================================
    # Sparkline Data
    # =====================================================

    def sparkline(self, integration):

        data = self.df[

            self.df["integration_system"]

            == integration

        ]

        spark = (

            data

            .groupby(

                data["event_date"].dt.date

            )

            .size()

            .reset_index(name="executions")

        )

        return spark

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        return {

            "daily": self.daily_trend(),

            "weekly": self.weekly_trend(),

            "monthly": self.monthly_trend(),

            "failure": self.failure_trend(),

            "success": self.success_trend(),

            "integration": self.integration_trend(),

            "ranking": self.trend_ranking(),

            "improved": self.most_improved(),

            "degraded": self.most_degraded()

        }


if __name__ == "__main__":

    from services.excel_parser import ExcelParser
    from services.data_cleaner import DataCleaner
    from services.data_merger import DataMerger

    parser = ExcelParser()

    frames = parser.load_all()

    cleaned = {

        k: DataCleaner(v).clean()

        for k, v in frames.items()

    }

    master = DataMerger(cleaned).merge()

    trend = TrendEngine(master)

    print(trend.trend_ranking().head())

    print(trend.daily_trend().head())