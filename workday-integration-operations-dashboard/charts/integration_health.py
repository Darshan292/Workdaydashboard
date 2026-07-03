"""
Enterprise Integration Health Bubble Chart
"""

import numpy as np
import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class IntegrationHealthChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Calculate Health
    # ============================================================

    def calculate(self):

        summary = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("integration_system", "count"),

                success=("is_success", "sum"),

                failures=("is_failed", "sum"),

                warnings=("is_warning", "sum"),

                avg_runtime=("processing_time_seconds", "mean"),

                max_runtime=("processing_time_seconds", "max"),

                avg_items=("items_processed", "mean")

            )

            .reset_index()

        )

        summary["success_rate"] = np.where(

            summary["executions"] == 0,

            0,

            (

                summary["success"]

                /

                summary["executions"]

                * 100

            )

        )

        summary["failure_rate"] = np.where(

            summary["executions"] == 0,

            0,

            (

                summary["failures"]

                /

                summary["executions"]

                * 100

            )

        )

        summary["health_score"] = (

            summary["success_rate"] * 0.60 +

            (100 - summary["failure_rate"]) * 0.25 +

            (100 - summary["avg_runtime"].clip(upper=100)) * 0.15

        ).clip(0, 100).round(2)

        return summary

    # ============================================================
    # Bubble Chart
    # ============================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Integration Health"

            )

        summary = self.calculate()

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=summary["avg_runtime"],

                y=summary["success_rate"],

                mode="markers+text",

                text=summary["integration_system"],

                textposition="top center",

                marker=dict(

                    size=np.sqrt(

                        summary["executions"]

                    ) * 6,

                    color=summary["health_score"],

                    colorscale="RdYlGn",

                    reversescale=False,

                    showscale=True,

                    colorbar=dict(

                        title="Health"

                    ),

                    line=dict(

                        color="white",

                        width=1

                    ),

                    opacity=0.85

                ),

                customdata=summary[

                    [

                        "executions",

                        "health_score",

                        "failure_rate",

                        "avg_items"

                    ]

                ],

                hovertemplate=

                "<b>%{text}</b><br>"

                "Average Runtime : %{x:.2f}s<br>"

                "Success Rate : %{y:.2f}%<br>"

                "Executions : %{customdata[0]}<br>"

                "Health Score : %{customdata[1]:.1f}<br>"

                "Failure Rate : %{customdata[2]:.2f}%<br>"

                "Avg Items : %{customdata[3]:,.0f}"

                "<extra></extra>"

            )

        )

        self.apply_layout(

            fig,

            "Integration Health Matrix",

            height=550,

            legend=False

        )

        self.style_xaxis(

            fig,

            "Average Processing Time (Seconds)"

        )

        self.style_yaxis(

            fig,

            "Success Rate (%)"

        )

        fig.add_hline(

            y=95,

            line_dash="dash",

            line_color=CURRENT_THEME["success"]

        )

        fig.add_vline(

            x=30,

            line_dash="dash",

            line_color=CURRENT_THEME["warning"]

        )

        fig.add_annotation(

            x=30,

            y=98,

            text="Target Zone",

            showarrow=False,

            font=dict(

                size=12

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

    chart = IntegrationHealthChart(master)

    fig = chart.build()

    fig.show(config=chart.config())