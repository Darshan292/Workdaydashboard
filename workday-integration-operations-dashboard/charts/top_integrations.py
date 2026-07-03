"""
Enterprise Top Integrations Lollipop Chart
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class TopIntegrationsChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self, top_n=10):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Top Integrations",

                template=CURRENT_THEME["template"]

            )

            return fig

        top = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("integration_system", "count"),

                success=("is_success", "sum"),

                failures=("is_failed", "sum")

            )

            .reset_index()

        )

        top["success_rate"] = (

            top["success"]

            / top["executions"]

            * 100

        ).round(2)

        top = (

            top

            .sort_values(

                "executions",

                ascending=False

            )

            .head(top_n)

            .sort_values(

                "executions"

            )

        )

        fig = go.Figure()

        # ==========================================
        # Lollipop Stems
        # ==========================================

        for _, row in top.iterrows():

            fig.add_shape(

                type="line",

                x0=0,

                x1=row["executions"],

                y0=row["integration_system"],

                y1=row["integration_system"],

                line=dict(

                    color="#D1D5DB",

                    width=4

                )

            )

        # ==========================================
        # Lollipop Heads
        # ==========================================

        fig.add_trace(

            go.Scatter(

                x=top["executions"],

                y=top["integration_system"],

                mode="markers+text",

                marker=dict(

                    size=18,

                    color=CURRENT_THEME["primary"],

                    line=dict(

                        width=2,

                        color="white"

                    )

                ),

                text=top["executions"],

                textposition="middle right",

                hovertemplate=

                "<b>%{y}</b><br>"

                "Executions : %{x}<br>"

                "Success Rate : %{customdata}%"

                "<extra></extra>",

                customdata=top["success_rate"]

            )

        )

        fig.update_layout(

            title=dict(

                text="Top Integrations by Executions",

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

                r=40,

                t=60,

                b=20

            ),

            showlegend=False,

            transition=dict(

                duration=600

            )

        )

        fig.update_xaxes(

            title="Executions",

            showgrid=True,

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

    chart = TopIntegrationsChart(master)

    fig = chart.build()

    fig.show()