"""
Enterprise Failure Treemap
"""

import pandas as pd
import plotly.express as px

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class FailureTreemapChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Failure Treemap"
            )

        failures = self.df[

            self.df["status"] == "Failed"

        ].copy()

        if failures.empty:

            return self.empty_figure(
                "Failure Treemap"
            )

        failures["failure_reason"] = (

            failures["errors_warnings"]

            .fillna("Unknown")

            .replace("", "Unknown")

        )

        summary = (

            failures

            .groupby(

                [

                    "failure_reason",

                    "integration_system"

                ]

            )

            .size()

            .reset_index(name="count")

        )

        fig = px.treemap(

            summary,

            path=[

                "failure_reason",

                "integration_system"

            ],

            values="count",

            color="count",

            color_continuous_scale=[

                "#FEE2E2",

                "#FCA5A5",

                "#EF4444",

                "#B91C1C"

            ]

        )

        fig.update_traces(

            hovertemplate=

            "<b>%{label}</b><br>"

            "Failures : %{value}"

            "<extra></extra>",

            textfont=dict(

                size=13

            ),

            marker=dict(

                cornerradius=6

            )

        )

        self.apply_layout(

            fig,

            "Failure Distribution Treemap",

            height=520,

            legend=False

        )

        fig.update_layout(

            coloraxis_colorbar=dict(

                title="Failures"

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

    chart = FailureTreemapChart(master)

    fig = chart.build()

    fig.show(config=chart.config())