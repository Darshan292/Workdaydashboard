"""
Enterprise Integration Ranking
"""

import numpy as np
import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class IntegrationRankingChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Calculate Ranking
    # ============================================================

    def calculate(self):

        summary = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("integration_system", "count"),

                success=("is_success", "sum"),

                failed=("is_failed", "sum"),

                warning=("is_warning", "sum"),

                avg_runtime=("processing_time_seconds", "mean")

            )

            .reset_index()

        )

        summary["success_rate"] = (

            summary["success"]

            /

            summary["executions"]

            * 100

        )

        summary["health_score"] = (

            summary["success_rate"] * 0.70 +

            (100 - summary["avg_runtime"].clip(upper=100)) * 0.30

        ).round(1)

        summary["rank"] = (

            summary["health_score"]

            .rank(

                ascending=False,

                method="dense"

            )

            .astype(int)

        )

        return (

            summary

            .sort_values(

                "health_score",

                ascending=False

            )

            .head(10)

        )

    # ============================================================
    # Trend Arrow
    # ============================================================

    @staticmethod
    def trend(failure_rate):

        if failure_rate < 5:

            return "🟢 ↑"

        elif failure_rate < 15:

            return "🟡 →"

        return "🔴 ↓"

    # ============================================================
    # Build
    # ============================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Integration Ranking"

            )

        ranking = self.calculate()

        ranking["failure_rate"] = (

            ranking["failed"]

            /

            ranking["executions"]

            * 100

        )

        medals = {

            1: "🥇",

            2: "🥈",

            3: "🥉"

        }

        labels = []

        for _, row in ranking.iterrows():

            badge = medals.get(

                row["rank"],

                f"#{row['rank']}"

            )

            labels.append(

                f"{badge} {row['integration_system']}"

            )

        colors = np.where(

            ranking["health_score"] >= 90,

            CURRENT_THEME["success"],

            np.where(

                ranking["health_score"] >= 75,

                CURRENT_THEME["warning"],

                CURRENT_THEME["danger"]

            )

        )

        fig = go.Figure(

            go.Bar(

                x=ranking["health_score"],

                y=labels,

                orientation="h",

                marker=dict(

                    color=colors

                ),

                text=[

                    f"{v:.1f}"

                    for v in ranking["health_score"]

                ],

                textposition="outside",

                customdata=np.stack(

                    [

                        ranking["executions"],

                        ranking["avg_runtime"],

                        ranking["failure_rate"]

                    ],

                    axis=1

                ),

                hovertemplate=

                "<b>%{y}</b><br>"

                "Health Score : %{x:.1f}<br>"

                "Executions : %{customdata[0]}<br>"

                "Average Runtime : %{customdata[1]:.2f}s<br>"

                "Failure Rate : %{customdata[2]:.2f}%"

                "<extra></extra>"

            )

        )

        self.apply_layout(

            fig,

            "Top Integration Ranking",

            height=600,

            legend=False

        )

        self.style_xaxis(

            fig,

            "Health Score"

        )

        self.style_yaxis(

            fig,

            ""

        )

        fig.update_layout(

            xaxis=dict(

                range=[0, 100]

            )

        )

        for _, row in ranking.iterrows():

            fig.add_annotation(

                x=row["health_score"] + 4,

                y=f"{medals.get(row['rank'], f'#{row['rank']}')} {row['integration_system']}",

                text=self.trend(

                    row["failure_rate"]

                ),

                showarrow=False,

                font=dict(

                    size=15

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

    chart = IntegrationRankingChart(master)

    fig = chart.build()

    fig.show(config=chart.config())