"""
Enterprise Runtime Distribution (Violin Plot)
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class RuntimeDistributionChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Runtime Distribution"
            )

        fig = go.Figure()

        statuses = [

            "Success",

            "Warning",

            "Failed"

        ]

        colors = {

            "Success": CURRENT_THEME["success"],

            "Warning": CURRENT_THEME["warning"],

            "Failed": CURRENT_THEME["danger"]

        }

        for status in statuses:

            subset = self.df[

                self.df["status"] == status

            ]

            if subset.empty:

                continue

            fig.add_trace(

                go.Violin(

                    y=subset["processing_time_seconds"],

                    x=[status] * len(subset),

                    name=status,

                    box_visible=True,

                    meanline_visible=True,

                    points="suspectedoutliers",

                    fillcolor=colors[status],

                    line=dict(

                        color=colors[status]

                    ),

                    opacity=0.75,

                    hovertemplate=

                    "<b>%{x}</b><br>"

                    "Runtime : %{y:.2f}s"

                    "<extra></extra>"

                )

            )

        self.apply_layout(

            fig,

            "Runtime Distribution",

            height=460

        )

        self.style_xaxis(

            fig,

            "Execution Status"

        )

        self.style_yaxis(

            fig,

            "Processing Time (Seconds)"

        )

        fig.update_layout(

            violinmode="group"

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

    chart = RuntimeDistributionChart(master)

    fig = chart.build()

    fig.show()