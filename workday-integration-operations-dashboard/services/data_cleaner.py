"""
Enterprise Data Cleaner
"""

import re
import numpy as np
import pandas as pd


class DataCleaner:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def clean(self):

        self.standardize_columns()

        self.clean_strings()

        self.clean_status()

        self.clean_dates()

        self.clean_processing_time()

        self.clean_items_processed()

        self.clean_messages()

        self.remove_duplicates()

        self.add_derived_columns()

        self.sort_data()

        return self.df

    def standardize_columns(self):

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    def clean_strings(self):

        object_cols = self.df.select_dtypes(include="object").columns

        for col in object_cols:

            self.df[col] = (

                self.df[col]

                .fillna("")

                .astype(str)

                .str.replace(r"\s+", " ", regex=True)

                .str.strip()

            )

    def clean_status(self):

        if "status" not in self.df.columns:
            return

        status = self.df["status"].fillna("").str.lower()

        self.df["status"] = "Unknown"

        self.df.loc[
            status.str.contains("completed") &
            ~status.str.contains("error"),
            "status"
        ] = "Success"

        self.df.loc[
            status.str.contains("error|failed|failure"),
            "status"
        ] = "Failed"

        self.df.loc[
            status.str.contains("warning|warn"),
            "status"
        ] = "Warning"

        self.df.loc[
            status.str.contains("running"),
            "status"
        ] = "Running"

        self.df.loc[
            status.str.contains("cancel"),
            "status"
        ] = "Cancelled"

    def clean_dates(self):

        if "event_date" not in self.df.columns:
            return

        self.df["event_date"] = pd.to_datetime(

            self.df["event_date"],

            errors="coerce"

        )

        self.df["date"] = self.df["event_date"].dt.date

        self.df["day"] = self.df["event_date"].dt.day_name()

        self.df["hour"] = self.df["event_date"].dt.hour

        self.df["week"] = self.df["event_date"].dt.isocalendar().week

        self.df["month"] = self.df["event_date"].dt.month_name()

        self.df["year"] = self.df["event_date"].dt.year

    def clean_processing_time(self):

        if "processing_time_seconds" not in self.df.columns:
            return

        self.df["processing_time_seconds"] = pd.to_numeric(

            self.df["processing_time_seconds"],

            errors="coerce"

        ).fillna(0)

        self.df["processing_time_minutes"] = (

            self.df["processing_time_seconds"] / 60

        ).round(2)

    def clean_items_processed(self):

        if "items_processed" not in self.df.columns:
            return

        self.df["items_processed"] = pd.to_numeric(

            self.df["items_processed"],

            errors="coerce"

        ).fillna(0)

    def clean_messages(self):

        cols = [

            "response_message",

            "errors_warnings",

            "messages"

        ]

        for col in cols:

            if col not in self.df.columns:
                continue

            self.df[col] = (

                self.df[col]

                .fillna("")

                .astype(str)

                .str.replace(r"<.*?>", "", regex=True)

                .str.replace(r"\s+", " ", regex=True)

                .str.strip()

            )

    def remove_duplicates(self):

        self.df.drop_duplicates(

            inplace=True,

            ignore_index=True

        )

    def add_derived_columns(self):

        if "status" in self.df.columns:

            self.df["is_success"] = (

                self.df["status"] == "Success"

            )

            self.df["is_failed"] = (

                self.df["status"] == "Failed"

            )

            self.df["is_warning"] = (

                self.df["status"] == "Warning"

            )

        if "processing_time_seconds" in self.df.columns:

            self.df["is_slow"] = (

                self.df["processing_time_seconds"] >= 30

            )

        if "integration_system" in self.df.columns:

            self.df["integration_name"] = (

                self.df["integration_system"]

                .str.replace(r"^INT\d+\s*", "", regex=True)

            )

    def sort_data(self):

        if "event_date" in self.df.columns:

            self.df.sort_values(

                "event_date",

                ascending=False,

                inplace=True,

                ignore_index=True

            )

    def summary(self):

        return {

            "rows": len(self.df),

            "columns": len(self.df.columns),

            "duplicates": int(self.df.duplicated().sum()),

            "missing": self.df.isna().sum().sum(),

            "success": int(self.df.get("is_success", pd.Series(dtype=bool)).sum()),

            "failed": int(self.df.get("is_failed", pd.Series(dtype=bool)).sum()),

            "warning": int(self.df.get("is_warning", pd.Series(dtype=bool)).sum())

        }


if __name__ == "__main__":

    from services.excel_parser import ExcelParser

    parser = ExcelParser()

    df = parser.get_merged_dataframe()

    cleaner = DataCleaner(df)

    cleaned = cleaner.clean()

    print(cleaner.summary())

    print(cleaned.head())