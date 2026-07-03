"""
Enterprise Runtime Outliers Chart
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class RuntimeOutliersChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Runtime Outliers"
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

            data = self.df[

                self.df["status"] == status

            ]

            if data.empty:

                continue

            fig.add_trace(

                go.Box(

                    y=data["processing_time_seconds"],

                    name=status,

                    boxpoints="outliers",

                    marker=dict(

                        color=colors[status],

                        size=6

                    ),

                    line=dict(

                        color=colors[status],

                        width=2

                    ),

                    fillcolor=colors[status],

                    opacity=0.60,

                    hovertemplate=

                    "<b>%{x}</b><br>"

                    "Runtime : %{y:.2f}s"

                    "<extra></extra>"

                )

            )

        self.apply_layout(

            fig,

            "Runtime Outliers",

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

    chart = RuntimeOutliersChart(master)

    fig = chart.build()

    fig.show()