"""
Enterprise Excel Parser
"""

from pathlib import Path
import pandas as pd

from config.settings import EXCEL_FILES


class ExcelParser:

    STANDARD_COLUMNS = {
        "Integration System": "integration_system",
        "Integration Event": "integration_event",
        "Integration Event Status": "status",
        "Integration Attachment": "attachment",
        "CF LRV Event Date": "event_date",
        "Items Processed": "items_processed",
        "Response Message": "response_message",
        "Errors & Warnings": "errors_warnings",
        "Messages": "messages",
        "Created From Integration Process Event": "parent_event",
        "Processing Time (s)": "processing_time_seconds",
    }

    REPORT_NAMES = {
        "Failure": "Failures",
        "Event Statistics": "Event Statistics",
        "higher processing": "Processing Time",
    }

    def __init__(self):
        self.frames = {}

    def load_all(self):
        """
        Load all configured Excel reports.
        """

        for file in EXCEL_FILES:

            if file.exists():

                report_name = self._identify_report(file.name)

                self.frames[report_name] = self.load_report(file, report_name)

            else:
                print(f"Warning: {file.name} not found.")

        return self.frames

    def load_report(self, file_path: Path, report_name: str):

        df = pd.read_excel(file_path, dtype=str)

        df = self._repair_header(df)

        df.columns = [str(c).strip() for c in df.columns]

        df.rename(columns=self.STANDARD_COLUMNS, inplace=True)

        df["report_type"] = report_name

        self._convert_types(df)

        return df

    def _repair_header(self, df):

        first_col = str(df.columns[0])

        if (
            "Integration System" not in first_col
            and len(df) > 0
            and str(df.iloc[0, 0]).strip() == "Integration System"
        ):

            df.columns = df.iloc[0]

            df = df.iloc[1:].reset_index(drop=True)

        return df

    def _convert_types(self, df):

        if "event_date" in df.columns:

            df["event_date"] = pd.to_datetime(
                df["event_date"],
                errors="coerce"
            )

        if "items_processed" in df.columns:

            df["items_processed"] = pd.to_numeric(
                df["items_processed"],
                errors="coerce"
            ).fillna(0)

        if "processing_time_seconds" in df.columns:

            df["processing_time_seconds"] = pd.to_numeric(
                df["processing_time_seconds"],
                errors="coerce"
            ).fillna(0)

        text_cols = [
            "integration_system",
            "integration_event",
            "status",
            "attachment",
            "response_message",
            "errors_warnings",
            "messages",
            "parent_event",
        ]

        for col in text_cols:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

    def _identify_report(self, filename):

        for key, value in self.REPORT_NAMES.items():

            if key.lower() in filename.lower():

                return value

        return "Unknown"

    def get_merged_dataframe(self):

        if not self.frames:

            self.load_all()

        merged = pd.concat(

            self.frames.values(),

            ignore_index=True,

            sort=False

        )

        merged.drop_duplicates(inplace=True)

        merged.reset_index(drop=True, inplace=True)

        return merged


if __name__ == "__main__":

    parser = ExcelParser()

    parser.load_all()

    df = parser.get_merged_dataframe()

    print("=" * 70)
    print(df.info())
    print("=" * 70)
    print(df.head())