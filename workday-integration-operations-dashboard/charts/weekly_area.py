"""
Enterprise Weekly Execution Trend
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class WeeklyAreaChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Weekly Trend",

                template=CURRENT_THEME["template"]

            )

            return fig

        weekly = (

            self.df

            .groupby(

                self.df["event_date"]

                .dt.to_period("W")

            )

            .agg(

                executions=("integration_system", "count"),

                avg_runtime=("processing_time_seconds", "mean")

            )

            .reset_index()

        )

        weekly["week"] = weekly["event_date"].astype(str)

        fig = go.Figure()

        # ===========================================
        # Execution Area
        # ===========================================

        fig.add_trace(

            go.Scatter(

                x=weekly["week"],

                y=weekly["executions"],

                mode="lines",

                fill="tozeroy",

                name="Executions",

                line=dict(

                    color=CURRENT_THEME["primary"],

                    width=4,

                    shape="spline"

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Executions : %{y}"

                "<extra></extra>"

            )

        )

        # ===========================================
        # Runtime Line
        # ===========================================

        fig.add_trace(

            go.Scatter(

                x=weekly["week"],

                y=weekly["avg_runtime"],

                mode="lines+markers",

                name="Avg Runtime",

                yaxis="y2",

                line=dict(

                    color=CURRENT_THEME["warning"],

                    width=3,

                    dash="dot"

                ),

                marker=dict(size=7)

            )

        )

        fig.update_layout(

            title=dict(

                text="Weekly Execution Trend",

                x=0.02,

                font=dict(size=20)

            ),

            template=CURRENT_THEME["template"],

            paper_bgcolor=CURRENT_THEME["paper"],

            plot_bgcolor=CURRENT_THEME["paper"],

            hovermode="x unified",

            height=420,

            margin=dict(

                l=20,

                r=20,

                t=60,

                b=20

            ),

            transition=dict(

                duration=600

            ),

            legend=dict(

                orientation="h",

                y=1.08,

                x=1,

                xanchor="right"

            ),

            yaxis=dict(

                title="Executions",

                gridcolor=CURRENT_THEME["grid"]

            ),

            yaxis2=dict(

                title="Avg Runtime (s)",

                overlaying="y",

                side="right",

                showgrid=False

            )

        )

        fig.update_xaxes(

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

    chart = WeeklyAreaChart(master)

    fig = chart.build()

    fig.show()