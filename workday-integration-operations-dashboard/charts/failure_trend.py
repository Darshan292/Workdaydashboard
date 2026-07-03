"""
Enterprise Failure Trend Chart
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class FailureTrendChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Failure Trend"
            )

        failures = (

            self.df[

                self.df["status"] == "Failed"

            ]

            .groupby(

                self.df["event_date"].dt.date

            )

            .size()

            .reset_index(name="failures")

        )

        if failures.empty:

            return self.empty_figure(
                "Failure Trend"
            )

        failures["rolling_avg"] = (

            failures["failures"]

            .rolling(

                window=3,

                min_periods=1

            )

            .mean()

        )

        peak_index = failures["failures"].idxmax()

        peak_date = failures.loc[peak_index, "event_date"]

        peak_value = failures.loc[peak_index, "failures"]

        fig = go.Figure()

        # ====================================================
        # Failure Area
        # ====================================================

        fig.add_trace(

            go.Scatter(

                x=failures["event_date"],

                y=failures["failures"],

                mode="lines",

                fill="tozeroy",

                name="Failures",

                line=dict(

                    color=CURRENT_THEME["danger"],

                    width=4,

                    shape="spline"

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Failures : %{y}"

                "<extra></extra>"

            )

        )

        # ====================================================
        # Rolling Average
        # ====================================================

        fig.add_trace(

            go.Scatter(

                x=failures["event_date"],

                y=failures["rolling_avg"],

                mode="lines",

                name="3-Day Average",

                line=dict(

                    color=CURRENT_THEME["warning"],

                    width=3,

                    dash="dash"

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Average : %{y:.2f}"

                "<extra></extra>"

            )

        )

        # ====================================================
        # Peak Annotation
        # ====================================================

        fig.add_annotation(

            x=peak_date,

            y=peak_value,

            text=f"Peak ({peak_value})",

            showarrow=True,

            arrowhead=2,

            ax=0,

            ay=-40,

            bgcolor=CURRENT_THEME["danger"],

            font=dict(

                color="white"

            )

        )

        self.apply_layout(

            fig,

            "Failure Trend",

            height=460

        )

        self.style_xaxis(

            fig,

            "Date"

        )

        self.style_yaxis(

            fig,

            "Failed Executions"

        )

        fig.update_layout(

            hovermode="x unified"

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

    chart = FailureTrendChart(master)

    fig = chart.build()

    fig.show()