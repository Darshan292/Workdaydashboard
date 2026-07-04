"""
Enterprise Success vs Failure Chart
"""

import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class SuccessFailureChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Build
    # ============================================================

    def build(self, top_n=15):

        if self.df.empty:

            return self.empty_figure(

                "Success vs Failure"

            )

        summary = (

            self.df

            .groupby("integration_system")

            .agg(

                Success=("is_success", "sum"),

                Warning=("is_warning", "sum"),

                Failed=("is_failed", "sum"),

                Total=("integration_system", "count")

            )

            .reset_index()

        )

        summary = (

            summary

            .sort_values(

                "Total",

                ascending=False

            )

            .head(top_n)

        )

        summary = summary.sort_values(

            "Success",

            ascending=True

        )

        summary["Success Rate"] = (

            summary["Success"]

            /

            summary["Total"]

            * 100

        ).round(1)

        fig = go.Figure()

        fig.add_trace(

            go.Bar(

                y=summary["integration_system"],

                x=summary["Success"],

                orientation="h",

                name="Success",

                marker=dict(

                    color=CURRENT_THEME["success"]

                ),

                customdata=summary[

                    [

                        "Success Rate",

                        "Total"

                    ]

                ],

                hovertemplate=

                "<b>%{y}</b><br>"

                "Success : %{x}<br>"

                "Success Rate : %{customdata[0]}%<br>"

                "Executions : %{customdata[1]}"

                "<extra></extra>"

            )

        )

        fig.add_trace(

            go.Bar(

                y=summary["integration_system"],

                x=summary["Warning"],

                orientation="h",

                name="Warning",

                marker=dict(

                    color=CURRENT_THEME["warning"]

                ),

                hovertemplate=

                "<b>%{y}</b><br>"

                "Warnings : %{x}"

                "<extra></extra>"

            )

        )

        fig.add_trace(

            go.Bar(

                y=summary["integration_system"],

                x=summary["Failed"],

                orientation="h",

                name="Failed",

                marker=dict(

                    color=CURRENT_THEME["danger"]

                ),

                hovertemplate=

                "<b>%{y}</b><br>"

                "Failures : %{x}"

                "<extra></extra>"

            )

        )

        self.apply_layout(

            fig,

            "Success vs Failure by Integration",

            height=600

        )

        self.style_xaxis(

            fig,

            "Execution Count"

        )

        self.style_yaxis(

            fig,

            ""

        )

        fig.update_layout(

            barmode="stack",

            legend=dict(

                orientation="h",

                y=1.08,

                x=1,

                xanchor="right"

            )

        )

        for _, row in summary.iterrows():

            fig.add_annotation(

                x=row["Total"],

                y=row["integration_system"],

                text=f"{row['Success Rate']}%",

                showarrow=False,

                xshift=25,

                font=dict(

                    size=11,

                    color=CURRENT_THEME["text"]

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

    chart = SuccessFailureChart(master)

    fig = chart.build()

    fig.show(config=chart.config())