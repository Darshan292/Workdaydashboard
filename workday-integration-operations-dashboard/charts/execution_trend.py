"""
Enterprise Execution Trend Chart
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class ExecutionTrendChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Execution Trend",

                template=CURRENT_THEME["template"]

            )

            return fig

        trend = (

            self.df

            .groupby(

                self.df["event_date"].dt.date

            )

            .size()

            .reset_index(name="executions")

            .rename(

                columns={

                    "event_date": "date"

                }

            )

        )

        trend["moving_average"] = (

            trend["executions"]

            .rolling(

                3,

                min_periods=1

            )

            .mean()

        )

        fig = go.Figure()

        # =====================================================
        # Execution Line
        # =====================================================

        fig.add_trace(

            go.Scatter(

                x=trend["date"],

                y=trend["executions"],

                mode="lines+markers",

                name="Executions",

                line=dict(

                    color=CURRENT_THEME["primary"],

                    width=4,

                    shape="spline"

                ),

                marker=dict(

                    size=8

                ),

                fill="tozeroy",

                hovertemplate=

                "<b>%{x}</b><br>"

                "Executions : %{y}"

                "<extra></extra>"

            )

        )

        # =====================================================
        # Moving Average
        # =====================================================

        fig.add_trace(

            go.Scatter(

                x=trend["date"],

                y=trend["moving_average"],

                mode="lines",

                name="Moving Avg",

                line=dict(

                    color=CURRENT_THEME["warning"],

                    width=3,

                    dash="dash"

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Average : %{y:.2f}"

                "<extra></extra>"

            )

        )

        # =====================================================
        # Layout
        # =====================================================

        fig.update_layout(

            title=dict(

                text="Execution Trend",

                x=0.02,

                font=dict(

                    size=20

                )

            ),

            template=CURRENT_THEME["template"],

            paper_bgcolor=CURRENT_THEME["paper"],

            plot_bgcolor=CURRENT_THEME["paper"],

            height=420,

            margin=dict(

                l=20,

                r=20,

                t=60,

                b=20

            ),

            hovermode="x unified",

            transition=dict(

                duration=600

            ),

            legend=dict(

                orientation="h",

                y=1.08,

                x=1,

                xanchor="right"

            )

        )

        fig.update_xaxes(

            showgrid=False,

            title=""

        )

        fig.update_yaxes(

            title="Executions",

            gridcolor=CURRENT_THEME["grid"],

            zeroline=False

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

    chart = ExecutionTrendChart(master)

    figure = chart.build()

    figure.show()