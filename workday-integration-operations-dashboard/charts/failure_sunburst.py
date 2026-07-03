"""
Enterprise Failure Sunburst Chart
"""

import plotly.express as px

from charts.base_chart import BaseChart


class FailureSunburstChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Failure Hierarchy"

            )

        failures = self.df[

            self.df["status"] == "Failed"

        ].copy()

        if failures.empty:

            return self.empty_figure(

                "Failure Hierarchy"

            )

        failures["failure_reason"] = (

            failures["errors_warnings"]

            .fillna("Unknown")

            .replace("", "Unknown")

        )

        failures["response"] = (

            failures["response_message"]

            .fillna("No Response")

            .replace("", "No Response")

            .str.slice(0, 60)

        )

        summary = (

            failures

            .groupby(

                [

                    "failure_reason",

                    "integration_system",

                    "response"

                ]

            )

            .size()

            .reset_index(name="count")

        )

        fig = px.sunburst(

            summary,

            path=[

                "failure_reason",

                "integration_system",

                "response"

            ],

            values="count",

            color="count",

            color_continuous_scale=[

                "#FEE2E2",

                "#FCA5A5",

                "#EF4444",

                "#991B1B"

            ]

        )

        fig.update_traces(

            insidetextorientation="radial",

            hovertemplate=

            "<b>%{label}</b><br>"

            "Occurrences : %{value}<br>"

            "Share : %{percentParent}"

            "<extra></extra>"

        )

        self.apply_layout(

            fig,

            "Failure Hierarchy",

            height=600,

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

    chart = FailureSunburstChart(master)

    fig = chart.build()

    fig.show(config=chart.config())