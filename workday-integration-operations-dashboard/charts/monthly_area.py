"""
Enterprise Monthly Trend Chart
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class MonthlyAreaChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Monthly Trend",

                template=CURRENT_THEME["template"]

            )

            return fig

        monthly = (

            self.df

            .groupby(

                self.df["event_date"]

                .dt.to_period("M")

            )

            .agg(

                success=(

                    "is_success",

                    "sum"

                ),

                failures=(

                    "is_failed",

                    "sum"

                ),

                warnings=(

                    "is_warning",

                    "sum"

                )

            )

            .reset_index()

        )

        monthly["month"] = (

            monthly["event_date"]

            .astype(str)

        )

        fig = go.Figure()

        # =======================================
        # Success
        # =======================================

        fig.add_trace(

            go.Scatter(

                x=monthly["month"],

                y=monthly["success"],

                stackgroup="one",

                mode="lines",

                name="Success",

                line=dict(

                    color=CURRENT_THEME["success"],

                    width=3,

                    shape="spline"

                ),

                hovertemplate=

                "<b>%{x}</b><br>"

                "Success : %{y}"

                "<extra></extra>"

            )

        )

        # =======================================
        # Warning
        # =======================================

        fig.add_trace(

            go.Scatter(

                x=monthly["month"],

                y=monthly["warnings"],

                stackgroup="one",

                mode="lines",

                name="Warning",

                line=dict(

                    color=CURRENT_THEME["warning"],

                    width=3,

                    shape="spline"

                )

            )

        )

        # =======================================
        # Failed
        # =======================================

        fig.add_trace(

            go.Scatter(

                x=monthly["month"],

                y=monthly["failures"],

                stackgroup="one",

                mode="lines",

                name="Failed",

                line=dict(

                    color=CURRENT_THEME["danger"],

                    width=3,

                    shape="spline"

                )

            )

        )

        fig.update_layout(

            title=dict(

                text="Monthly Execution Trend",

                x=0.02,

                font=dict(

                    size=20

                )

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

                x=1,

                xanchor="right",

                y=1.08

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

    chart = MonthlyAreaChart(master)

    fig = chart.build()

    fig.show()