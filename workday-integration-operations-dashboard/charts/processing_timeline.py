"""
Enterprise Processing Timeline
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class ProcessingTimelineChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Processing Timeline"
            )

        colors = {

            "Success": CURRENT_THEME["success"],

            "Warning": CURRENT_THEME["warning"],

            "Failed": CURRENT_THEME["danger"],

            "Running": CURRENT_THEME["primary"],

            "Cancelled": CURRENT_THEME["secondary"]

        }

        fig = go.Figure()

        statuses = self.df["status"].dropna().unique()

        for status in statuses:

            subset = self.df[
                self.df["status"] == status
            ]

            bubble_size = (

                subset["items_processed"]

                .fillna(0)

                .clip(lower=1)

                .pow(0.35)

                * 8

            )

            fig.add_trace(

                go.Scatter(

                    x=subset["event_date"],

                    y=subset["processing_time_seconds"],

                    mode="markers",

                    name=status,

                    marker=dict(

                        size=bubble_size,

                        color=colors.get(

                            status,

                            CURRENT_THEME["info"]

                        ),

                        opacity=0.75,

                        line=dict(

                            color="white",

                            width=1

                        )

                    ),

                    customdata=subset[

                        [

                            "integration_system",

                            "integration_event",

                            "items_processed",

                            "response_message"

                        ]

                    ],

                    hovertemplate=

                    "<b>%{customdata[0]}</b><br>"

                    "Event : %{customdata[1]}<br>"

                    "Runtime : %{y:.2f}s<br>"

                    "Items : %{customdata[2]}<br>"

                    "Status : "

                    + status +

                    "<br>"

                    "Response : %{customdata[3]}"

                    "<extra></extra>"

                )

            )

        self.apply_layout(

            fig,

            "Processing Timeline",

            height=500

        )

        self.style_xaxis(

            fig,

            "Execution Time"

        )

        self.style_yaxis(

            fig,

            "Processing Time (Seconds)"

        )

        fig.update_layout(

            hovermode="closest",

            legend=dict(

                orientation="h",

                y=1.08,

                x=1,

                xanchor="right"

            )

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

    chart = ProcessingTimelineChart(master)

    fig = chart.build()

    fig.show()