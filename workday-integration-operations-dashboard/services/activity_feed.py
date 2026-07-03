"""
Enterprise Activity Feed Service
"""

import pandas as pd


class ActivityFeed:

    def __init__(self, df):

        self.df = df.copy()

        self.df["event_date"] = pd.to_datetime(
            self.df["event_date"],
            errors="coerce"
        )

        self.df.sort_values(
            "event_date",
            ascending=False,
            inplace=True
        )

    # =====================================================
    # Severity
    # =====================================================

    @staticmethod
    def severity(status):

        if status == "Failed":
            return "Critical"

        if status == "Warning":
            return "Warning"

        if status == "Running":
            return "Running"

        if status == "Cancelled":
            return "Cancelled"

        return "Success"

    # =====================================================
    # Badge Color
    # =====================================================

    @staticmethod
    def badge(severity):

        mapping = {

            "Critical": "danger",

            "Warning": "warning",

            "Running": "primary",

            "Cancelled": "secondary",

            "Success": "success"

        }

        return mapping.get(
            severity,
            "secondary"
        )

    # =====================================================
    # Relative Time
    # =====================================================

    @staticmethod
    def relative_time(dt):

        if pd.isna(dt):
            return ""

        now = pd.Timestamp.now()

        diff = now - dt

        if diff.days > 0:
            return f"{diff.days}d ago"

        hours = diff.seconds // 3600

        if hours > 0:
            return f"{hours}h ago"

        minutes = diff.seconds // 60

        if minutes > 0:
            return f"{minutes}m ago"

        return "Just now"

    # =====================================================
    # Build Feed
    # =====================================================

    def build(self, limit=50):

        activities = []

        for _, row in self.df.head(limit).iterrows():

            severity = self.severity(
                row.get("status", "")
            )

            activities.append({

                "timestamp":

                    row.get("event_date"),

                "relative_time":

                    self.relative_time(
                        row.get("event_date")
                    ),

                "integration":

                    row.get(
                        "integration_system",
                        ""
                    ),

                "event":

                    row.get(
                        "integration_event",
                        ""
                    ),

                "status":

                    row.get(
                        "status",
                        ""
                    ),

                "severity":

                    severity,

                "badge":

                    self.badge(
                        severity
                    ),

                "processing_time":

                    row.get(
                        "processing_time_seconds",
                        0
                    ),

                "items_processed":

                    row.get(
                        "items_processed",
                        0
                    ),

                "response":

                    row.get(
                        "response_message",
                        ""
                    ),

                "errors":

                    row.get(
                        "errors_warnings",
                        ""
                    ),

                "messages":

                    row.get(
                        "messages",
                        ""
                    )

            })

        return activities

    # =====================================================
    # Critical Feed
    # =====================================================

    def critical(self, limit=20):

        failed = self.df[

            self.df["status"] == "Failed"

        ]

        return ActivityFeed(

            failed

        ).build(limit)

    # =====================================================
    # Warning Feed
    # =====================================================

    def warnings(self, limit=20):

        warnings = self.df[

            self.df["status"] == "Warning"

        ]

        return ActivityFeed(

            warnings

        ).build(limit)

    # =====================================================
    # Latest Executions
    # =====================================================

    def latest(self, limit=20):

        return self.build(limit)

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        return {

            "activities":

                len(self.df),

            "latest":

                self.latest(10),

            "critical":

                self.critical(10),

            "warnings":

                self.warnings(10)

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

    feed = ActivityFeed(master)

    from pprint import pprint

    pprint(feed.latest(5))