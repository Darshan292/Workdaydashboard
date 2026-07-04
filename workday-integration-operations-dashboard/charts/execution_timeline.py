"""
Enterprise Execution Timeline (Gantt Style)
"""

import pandas as pd
import plotly.express as px

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class ExecutionTimelineChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Prepare Timeline
    # ============================================================

    def prepare(self):

        df = self.df.copy()

        df["start"] = pd.to_datetime(

            df["event_date"],

            errors="coerce"

        )

        df["processing_time_seconds"] = (

            pd.to_numeric(

                df["processing_time_seconds"],

                errors="coerce"

            )

            .fillna(1)

            .clip(lower=1)

        )

        df["end"] = (

            df["start"]

            +

            pd.to_timedelta(

                df["processing_time_seconds"],

                unit="s"

            )

        )

        df["duration"] = (

            df["processing_time_seconds"]

            .round(2)

        )

        return df

    # ============================================================
    # Build Timeline
    # ============================================================

    def build(self, top_n=200):

        if self.df.empty:

            return self.empty_figure(

                "Execution Timeline"

            )

        timeline = self.prepare()

        timeline = (

            timeline

            .sort_values(

                "start",

                ascending=False

            )

            .head(top_n)

        )

        color_map = {

            "Success": CURRENT_THEME["success"],

            "Warning": CURRENT_THEME["warning"],

            "Failed": CURRENT_THEME["danger"],

            "Running": CURRENT_THEME["primary"],

            "Cancelled": CURRENT_THEME["secondary"]

        }

        fig = px.timeline(

            timeline,

            x_start="start",

            x_end="end",

            y="integration_system",

            color="status",

            color_discrete_map=color_map,

            hover_data={

                "integration_event": True,

                "duration": True,

                "items_processed": True,

                "response_message": True,

                "start": False,

                "end": False

            }

        )

        fig.update_yaxes(

            autorange="reversed"

        )

        fig.update_traces(

            hovertemplate=

            "<b>%{y}</b><br>"

            "Status : %{customdata[0]}<br>"

            "Duration : %{customdata[2]} sec<br>"

            "Items : %{customdata[3]}<br>"

            "Response : %{customdata[4]}"

            "<extra></extra>"

        )

        self.apply_layout(

            fig,

            "Execution Timeline",

            height=650

        )

        self.style_xaxis(

            fig,

            "Execution Time"

        )

        self.style_yaxis(

            fig,

            ""

        )

        return fig

    @staticmethod
    def config():

        return BaseChart.config()


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

    chart = ExecutionTimelineChart(master)

    fig = chart.build()

    fig.show(config=chart.config())