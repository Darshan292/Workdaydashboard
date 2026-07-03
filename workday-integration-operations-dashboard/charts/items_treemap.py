"""
Enterprise Items Processed Treemap
"""

import plotly.express as px

from charts.base_chart import BaseChart


class ItemsTreemapChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Build Treemap
    # ============================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Items Processed"

            )

        summary = (

            self.df

            .groupby("integration_system")

            .agg(

                items_processed=(

                    "items_processed",

                    "sum"

                ),

                executions=(

                    "integration_system",

                    "count"

                ),

                avg_runtime=(

                    "processing_time_seconds",

                    "mean"

                ),

                success=(

                    "is_success",

                    "sum"

                )

            )

            .reset_index()

        )

        summary["success_rate"] = (

            summary["success"]

            /

            summary["executions"]

            * 100

        ).round(2)

        fig = px.treemap(

            summary,

            path=[

                "integration_system"

            ],

            values="items_processed",

            color="avg_runtime",

            color_continuous_scale=[

                "#22C55E",

                "#84CC16",

                "#FACC15",

                "#F97316",

                "#DC2626"

            ],

            custom_data=[

                "executions",

                "avg_runtime",

                "success_rate"

            ]

        )

        fig.update_traces(

            textinfo="label+value",

            hovertemplate=

            "<b>%{label}</b><br>"

            "Items Processed : %{value:,.0f}<br>"

            "Executions : %{customdata[0]}<br>"

            "Average Runtime : %{customdata[1]:.2f}s<br>"

            "Success Rate : %{customdata[2]:.2f}%"

            "<extra></extra>",

            marker=dict(

                cornerradius=6

            )

        )

        self.apply_layout(

            fig,

            "Items Processed Distribution",

            height=550,

            legend=False

        )

        fig.update_layout(

            coloraxis_colorbar=dict(

                title="Avg Runtime (s)"

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

    chart = ItemsTreemapChart(master)

    fig = chart.build()

    fig.show(config=chart.config())