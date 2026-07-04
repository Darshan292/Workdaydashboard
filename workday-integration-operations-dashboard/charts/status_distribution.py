"""
Enterprise Status Distribution Chart
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class StatusDistributionChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Execution Status",

                template=CURRENT_THEME["template"]

            )

            return fig

        status = (

            self.df

            .groupby("status")

            .size()

            .reset_index(name="count")

            .sort_values(

                "count",

                ascending=False

            )

        )

        color_map = {

            "Success": CURRENT_THEME["success"],

            "Failed": CURRENT_THEME["danger"],

            "Warning": CURRENT_THEME["warning"],

            "Running": CURRENT_THEME["primary"],

            "Cancelled": CURRENT_THEME["secondary"]

        }

        colors = [

            color_map.get(

                x,

                CURRENT_THEME["info"]

            )

            for x in status["status"]

        ]

        fig = go.Figure(

            go.Pie(

                labels=status["status"],

                values=status["count"],

                hole=0.72,

                sort=False,

                marker=dict(

                    colors=colors,

                    line=dict(

                        color=CURRENT_THEME["paper"],

                        width=3

                    )

                ),

                textinfo="percent",

                textfont=dict(

                    size=14,

                    color=CURRENT_THEME["text"]

                ),

                hovertemplate=

                "<b>%{label}</b><br>"

                "Executions: %{value}<br>"

                "Percentage: %{percent}"

                "<extra></extra>"

            )

        )

        total = int(status["count"].sum())

        fig.add_annotation(

            text=f"<b>{total}</b><br>Total",

            showarrow=False,

            font=dict(

                size=20,

                color=CURRENT_THEME["text"]

            )

        )

        fig.update_layout(

            title=dict(

                text="Execution Status Distribution",

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

            transition=dict(

                duration=600

            ),

            legend=dict(

                orientation="h",

                y=-0.12,

                x=0.5,

                xanchor="center"

            )

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

    chart = StatusDistributionChart(master)

    fig = chart.build()

    fig.show()