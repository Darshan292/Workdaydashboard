"""
Enterprise Hourly Execution Trend
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class HourlyTrendChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Hourly Execution Pattern",

                template=CURRENT_THEME["template"]

            )

            return fig

        self.df["hour"] = self.df["event_date"].dt.hour

        hourly = (

            self.df

            .groupby("hour")

            .size()

            .reindex(range(24), fill_value=0)

            .reset_index(name="executions")

        )

        hourly["theta"] = hourly["hour"] * 15

        fig = go.Figure()

        fig.add_trace(

            go.Scatterpolar(

                r=hourly["executions"],

                theta=hourly["theta"],

                mode="lines+markers",

                fill="toself",

                line=dict(

                    color=CURRENT_THEME["primary"],

                    width=4,

                    shape="spline"

                ),

                marker=dict(

                    size=8,

                    color=CURRENT_THEME["primary"]

                ),

                hovertemplate=

                "<b>%{customdata}:00</b><br>"

                "Executions : %{r}"

                "<extra></extra>",

                customdata=hourly["hour"]

            )

        )

        fig.update_layout(

            title=dict(

                text="Hourly Execution Pattern",

                x=0.02,

                font=dict(size=20)

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

            polar=dict(

                bgcolor=CURRENT_THEME["paper"],

                radialaxis=dict(

                    visible=True,

                    gridcolor=CURRENT_THEME["grid"],

                    ticks=""

                ),

                angularaxis=dict(

                    direction="clockwise",

                    rotation=90,

                    tickmode="array",

                    tickvals=[

                        0,

                        45,

                        90,

                        135,

                        180,

                        225,

                        270,

                        315

                    ],

                    ticktext=[

                        "00",

                        "03",

                        "06",

                        "09",

                        "12",

                        "15",

                        "18",

                        "21"

                    ]

                )

            ),

            showlegend=False,

            transition=dict(

                duration=600

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

    chart = HourlyTrendChart(master)

    fig = chart.build()

    fig.show()