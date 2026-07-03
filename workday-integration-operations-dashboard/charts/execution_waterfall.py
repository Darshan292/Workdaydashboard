"""
Enterprise Execution Waterfall
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class ExecutionWaterfallChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Build Waterfall
    # ============================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Execution Waterfall"

            )

        total = len(self.df)

        success = (

            self.df["status"]

            == "Success"

        ).sum()

        warning = (

            self.df["status"]

            == "Warning"

        ).sum()

        failed = (

            self.df["status"]

            == "Failed"

        ).sum()

        running = (

            self.df["status"]

            == "Running"

        ).sum()

        cancelled = (

            self.df["status"]

            == "Cancelled"

        ).sum()

        completed = success + warning

        fig = go.Figure(

            go.Waterfall(

                orientation="v",

                measure=[

                    "absolute",

                    "relative",

                    "relative",

                    "relative",

                    "relative",

                    "relative",

                    "total"

                ],

                x=[

                    "Total",

                    "Success",

                    "Warnings",

                    "Failures",

                    "Running",

                    "Cancelled",

                    "Completed"

                ],

                y=[

                    total,

                    -success,

                    -warning,

                    failed,

                    running,

                    cancelled,

                    0

                ],

                text=[

                    f"{total:,}",

                    f"{success:,}",

                    f"{warning:,}",

                    f"{failed:,}",

                    f"{running:,}",

                    f"{cancelled:,}",

                    f"{completed:,}"

                ],

                textposition="outside",

                connector=dict(

                    line=dict(

                        color="#94A3B8",

                        width=2

                    )

                ),

                increasing=dict(

                    marker=dict(

                        color=CURRENT_THEME["danger"]

                    )

                ),

                decreasing=dict(

                    marker=dict(

                        color=CURRENT_THEME["success"]

                    )

                ),

                totals=dict(

                    marker=dict(

                        color=CURRENT_THEME["primary"]

                    )

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Count : %{text}"

                "<extra></extra>"

            )

        )

        self.apply_layout(

            fig,

            "Execution Flow Summary",

            height=500,

            legend=False

        )

        self.style_yaxis(

            fig,

            "Execution Count"

        )

        self.style_xaxis(

            fig

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

    chart = ExecutionWaterfallChart(master)

    fig = chart.build()

    fig.show(config=chart.config())