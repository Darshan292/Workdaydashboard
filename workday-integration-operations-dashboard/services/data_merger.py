"""
Enterprise Data Merger
"""

import pandas as pd


class DataMerger:

    def __init__(self, frames: dict):

        self.frames = frames

    def merge(self):

        failures = self.frames.get("Failures", pd.DataFrame()).copy()

        events = self.frames.get("Event Statistics", pd.DataFrame()).copy()

        processing = self.frames.get("Processing Time", pd.DataFrame()).copy()

        failures = self.prepare_failures(failures)

        events = self.prepare_events(events)

        processing = self.prepare_processing(processing)

        master = pd.concat(

            [

                failures,

                events,

                processing

            ],

            ignore_index=True,

            sort=False

        )

        master = self.normalize(master)

        return master

    def prepare_failures(self, df):

        if df.empty:
            return df

        df["source"] = "Failures"

        return df

    def prepare_events(self, df):

        if df.empty:
            return df

        df["source"] = "Event Statistics"

        return df

    def prepare_processing(self, df):

        if df.empty:
            return df

        df["source"] = "Processing Time"

        return df

    def normalize(self, df):

        required_columns = [

            "integration_system",

            "integration_name",

            "integration_event",

            "status",

            "event_date",

            "items_processed",

            "processing_time_seconds",

            "response_message",

            "errors_warnings",

            "messages",

            "report_type",

            "source"

        ]

        for col in required_columns:

            if col not in df.columns:

                df[col] = None

        df["integration_name"] = (

            df["integration_name"]

            .fillna(df["integration_system"])

        )

        df["status"] = (

            df["status"]

            .replace("", "Unknown")

            .fillna("Unknown")

        )

        df["processing_time_seconds"] = (

            pd.to_numeric(

                df["processing_time_seconds"],

                errors="coerce"

            )

            .fillna(0)

        )

        df["items_processed"] = (

            pd.to_numeric(

                df["items_processed"],

                errors="coerce"

            )

            .fillna(0)

        )

        df["event_date"] = pd.to_datetime(

            df["event_date"],

            errors="coerce"

        )

        df = df.sort_values(

            "event_date",

            ascending=False,

            ignore_index=True

        )

        df["execution_id"] = range(

            1,

            len(df) + 1

        )

        df["health_score"] = 100

        df["trend"] = "Stable"

        df["risk"] = "Low"

        return df

    def validate(self, df):

        print("=" * 70)

        print("MASTER DATASET")

        print("=" * 70)

        print(f"Rows : {len(df)}")

        print(f"Columns : {len(df.columns)}")

        print()

        print(df.dtypes)

        print()

        print(df.head())

        print("=" * 70)


if __name__ == "__main__":

    from services.excel_parser import ExcelParser

    from services.data_cleaner import DataCleaner

    parser = ExcelParser()

    frames = parser.load_all()

    cleaned = {}

    for name, frame in frames.items():

        cleaned[name] = DataCleaner(frame).clean()

    merger = DataMerger(cleaned)

    master = merger.merge()

    merger.validate(master)