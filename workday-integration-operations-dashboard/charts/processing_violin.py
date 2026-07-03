"""
Enterprise Processing Time Violin Chart
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class ProcessingViolinChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Integration Category
    # ============================================================

    def classify(self, runtime):

        if runtime <= 10:
            return "Fast"

        elif runtime <= 30:
            return "Normal"

        elif runtime <= 60:
            return "Slow"

        return "Very Slow"

    # ============================================================
    # Build
    # ============================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Processing Time Distribution"

            )

        data = self.df.copy()

        data["runtime_class"] = data[
            "processing_time_seconds"
        ].apply(self.classify)

        colors = {

            "Fast": CURRENT_THEME["success"],

            "Normal": CURRENT_THEME["primary"],

            "Slow": CURRENT_THEME["warning"],

            "Very Slow": CURRENT_THEME["danger"]

        }

        fig = go.Figure()

        order = [

            "Fast",

            "Normal",

            "Slow",

            "Very Slow"

        ]

        for category in order:

            subset = data[

                data["runtime_class"]

                == category

            ]

            if subset.empty:

                continue

            fig.add_trace(

                go.Violin(

                    x=subset["runtime_class"],

                    y=subset["processing_time_seconds"],

                    name=category,

                    box_visible=True,

                    meanline_visible=True,

                    points="outliers",

                    pointpos=0,

                    side="positive",

                    width=0.8,

                    fillcolor=colors[category],

                    line=dict(

                        color=colors[category],

                        width=2

                    ),

                    opacity=0.75,

                    customdata=subset[

                        [

                            "integration_system",

                            "status",

                            "items_processed"

                        ]

                    ],

                    hovertemplate=

                    "<b>%{customdata[0]}</b><br>"

                    "Runtime : %{y:.2f}s<br>"

                    "Status : %{customdata[1]}<br>"

                    "Items : %{customdata[2]}"

                    "<extra></extra>"

                )

            )

        self.apply_layout(

            fig,

            "Processing Time Distribution",

            height=520

        )

        self.style_xaxis(

            fig,

            "Runtime Classification"

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

    chart = ProcessingViolinChart(master)

    fig = chart.build()

    fig.show(config=chart.config())