"""
Enterprise Integration Trend Ranking
"""

import numpy as np
import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class TrendRankingChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ==========================================================
    # Calculate Trend
    # ==========================================================

    def calculate(self):

        df = self.df.copy()

        df["day"] = df["event_date"].dt.date

        failures = (

            df

            .groupby(

                [

                    "integration_system",

                    "day"

                ]

            )

            .agg(

                failures=("is_failed", "sum"),

                executions=("integration_system", "count"),

                runtime=("processing_time_seconds", "mean")

            )

            .reset_index()

        )

        records = []

        for integration, group in failures.groupby(

            "integration_system"

        ):

            group = group.sort_values("day")

            first = group.iloc[0]

            last = group.iloc[-1]

            delta = (

                last["failures"]

                -

                first["failures"]

            )

            pct = (

                0

                if first["failures"] == 0

                else

                (delta / first["failures"]) * 100

            )

            records.append(

                {

                    "integration_system": integration,

                    "first_failures": first["failures"],

                    "last_failures": last["failures"],

                    "change": delta,

                    "change_percent": round(pct, 1),

                    "runtime": group["runtime"].mean(),

                    "executions": group["executions"].sum()

                }

            )

        return (

            self.df.__class__(records)

            .sort_values(

                "change"

            )

        )

    # ==========================================================
    # Trend Arrow
    # ==========================================================

    @staticmethod
    def arrow(change):

        if change < 0:

            return "🟢 ▼ Improved"

        elif change > 0:

            return "🔴 ▲ Worse"

        return "🟡 ► Stable"

    # ==========================================================
    # Build
    # ==========================================================

    def build(self, top_n=15):

        if self.df.empty:

            return self.empty_figure(

                "Integration Trend"

            )

        trend = self.calculate()

        trend = trend.tail(top_n)

        colors = np.where(

            trend["change"] > 0,

            CURRENT_THEME["danger"],

            np.where(

                trend["change"] < 0,

                CURRENT_THEME["success"],

                CURRENT_THEME["warning"]

            )

        )

        fig = go.Figure(

            go.Bar(

                x=trend["change"],

                y=trend["integration_system"],

                orientation="h",

                marker=dict(

                    color=colors

                ),

                customdata=np.stack(

                    [

                        trend["change_percent"],

                        trend["runtime"],

                        trend["executions"]

                    ],

                    axis=1

                ),

                hovertemplate=

                "<b>%{y}</b><br>"

                "Failure Change : %{x}<br>"

                "Trend : %{customdata[0]}%<br>"

                "Average Runtime : %{customdata[1]:.2f}s<br>"

                "Executions : %{customdata[2]}"

                "<extra></extra>"

            )

        )

        self.apply_layout(

            fig,

            "Failure Trend Ranking",

            height=620,

            legend=False

        )

        self.style_xaxis(

            fig,

            "Failure Change"

        )

        self.style_yaxis(

            fig,

            ""

        )

        fig.add_vline(

            x=0,

            line_dash="dash",

            line_color=CURRENT_THEME["secondary"]

        )

        for _, row in trend.iterrows():

            fig.add_annotation(

                x=row["change"],

                y=row["integration_system"],

                text=self.arrow(

                    row["change"]

                ),

                showarrow=False,

                xshift=45 if row["change"] >= 0 else -45,

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

    chart = TrendRankingChart(master)

    fig = chart.build()

    fig.show(config=chart.config())