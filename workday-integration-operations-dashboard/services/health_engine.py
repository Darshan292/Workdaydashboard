"""
Enterprise Integration Health Engine
"""

import numpy as np
import pandas as pd


class HealthEngine:

    def __init__(self, df):

        self.df = df.copy()

    # ======================================================
    # Integration Health
    # ======================================================

    def calculate(self):

        health = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("status", "count"),

                success=("is_success", "sum"),

                failures=("is_failed", "sum"),

                warnings=("is_warning", "sum"),

                avg_runtime=("processing_time_seconds", "mean"),

                max_runtime=("processing_time_seconds", "max"),

                avg_items=("items_processed", "mean")

            )

            .reset_index()

        )

        health["success_rate"] = np.where(

            health["executions"] == 0,

            0,

            round(

                health["success"]

                / health["executions"]

                * 100,

                2

            )

        )

        health["failure_rate"] = np.where(

            health["executions"] == 0,

            0,

            round(

                health["failures"]

                / health["executions"]

                * 100,

                2

            )

        )

        health["runtime_score"] = (

            100

            -

            (

                health["avg_runtime"] / 2

            )

        ).clip(0, 100)

        health["failure_score"] = (

            100

            -

            (

                health["failure_rate"] * 2

            )

        ).clip(0, 100)

        health["warning_score"] = (

            100

            -

            (

                health["warnings"] * 1.5

            )

        ).clip(0, 100)

        health["health_score"] = (

            (

                health["success_rate"] * 0.50

            )

            +

            (

                health["runtime_score"] * 0.25

            )

            +

            (

                health["failure_score"] * 0.15

            )

            +

            (

                health["warning_score"] * 0.10

            )

        ).round(2)

        health["health_status"] = np.select(

            [

                health["health_score"] >= 95,

                health["health_score"] >= 85,

                health["health_score"] >= 70,

                health["health_score"] >= 50

            ],

            [

                "Excellent",

                "Healthy",

                "Warning",

                "Critical"

            ],

            default="Failed"

        )

        health["risk"] = np.select(

            [

                health["health_score"] >= 90,

                health["health_score"] >= 75,

                health["health_score"] >= 60

            ],

            [

                "Low",

                "Medium",

                "High"

            ],

            default="Critical"

        )

        return health

    # ======================================================
    # Top Healthy
    # ======================================================

    def healthiest(self, limit=10):

        return (

            self.calculate()

            .sort_values(

                "health_score",

                ascending=False

            )

            .head(limit)

        )

    # ======================================================
    # Least Healthy
    # ======================================================

    def unhealthy(self, limit=10):

        return (

            self.calculate()

            .sort_values(

                "health_score"

            )

            .head(limit)

        )

    # ======================================================
    # Health Distribution
    # ======================================================

    def distribution(self):

        return (

            self.calculate()

            .groupby("health_status")

            .size()

            .reset_index(name="count")

        )

    # ======================================================
    # Dashboard Summary
    # ======================================================

    def summary(self):

        health = self.calculate()

        return {

            "average_health_score":

                round(

                    health["health_score"].mean(),

                    2

                ),

            "excellent":

                (

                    health["health_status"]

                    == "Excellent"

                ).sum(),

            "healthy":

                (

                    health["health_status"]

                    == "Healthy"

                ).sum(),

            "warning":

                (

                    health["health_status"]

                    == "Warning"

                ).sum(),

            "critical":

                (

                    health["health_status"]

                    == "Critical"

                ).sum(),

            "failed":

                (

                    health["health_status"]

                    == "Failed"

                ).sum()

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

    engine = HealthEngine(master)

    print(engine.calculate().head())

    print(engine.summary())