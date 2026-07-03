"""
Enterprise Slow Integrations Lollipop Chart
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class SlowIntegrationsChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self, top_n=10):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Slow Integrations",

                template=CURRENT_THEME["template"]

            )

            return fig

        runtime = (

            self.df

            .groupby("integration_system")

            .agg(

                avg_runtime=("processing_time_seconds", "mean"),

                max_runtime=("processing_time_seconds", "max"),

                executions=("integration_system", "count")

            )

            .reset_index()

            .sort_values(

                "avg_runtime",

                ascending=False

            )

            .head(top_n)

            .sort_values(

                "avg_runtime"

            )

        )

        fig = go.Figure()

        # ====================================================
        # Lollipop stems
        # ====================================================

        for _, row in runtime.iterrows():

            fig.add_shape(

                type="line",

                x0=0,

                x1=row["avg_runtime"],

                y0=row["integration_system"],

                y1=row["integration_system"],

                line=dict(

                    color="#CBD5E1",

                    width=4

                )

            )

        # ====================================================
        # Lollipop heads
        # ====================================================

        fig.add_trace(

            go.Scatter(

                x=runtime["avg_runtime"],

                y=runtime["integration_system"],

                mode="markers+text",

                text=[

                    f"{v:.1f}s"

                    for v in runtime["avg_runtime"]

                ],

                textposition="middle right",

                marker=dict(

                    size=20,

                    color=runtime["avg_runtime"],

                    colorscale="Turbo",

                    showscale=True,

                    colorbar=dict(

                        title="Avg Runtime"

                    ),

                    line=dict(

                        color="white",

                        width=2

                    )

                ),

                customdata=runtime[

                    [

                        "max_runtime",

                        "executions"

                    ]

                ],

                hovertemplate=

                "<b>%{y}</b><br>"

                "Average Runtime : %{x:.2f}s<br>"

                "Maximum Runtime : %{customdata[0]:.2f}s<br>"

                "Executions : %{customdata[1]}"

                "<extra></extra>"

            )

        )

        fig.update_layout(

            title=dict(

                text="Slowest Integrations",

                x=0.02,

                font=dict(

                    size=20

                )

            ),

            template=CURRENT_THEME["template"],

            paper_bgcolor=CURRENT_THEME["paper"],

            plot_bgcolor=CURRENT_THEME["paper"],

            height=500,

            margin=dict(

                l=20,

                r=70,

                t=60,

                b=20

            ),

            transition=dict(

                duration=600

            ),

            showlegend=False

        )

        fig.update_xaxes(

            title="Average Runtime (Seconds)",

            gridcolor=CURRENT_THEME["grid"],

            zeroline=False

        )

        fig.update_yaxes(

            title="",

            showgrid=False

        )

        return fig


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

    chart = SlowIntegrationsChart(master)

    fig = chart.build()

    fig.show()