"""
Enterprise Weekday vs Hour Heatmap
"""

import pandas as pd
import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class WeekdayHeatmapChart:

    def __init__(self, dataframe):

        self.df = dataframe.copy()

        self.df["event_date"] = pd.to_datetime(
            self.df["event_date"],
            errors="coerce"
        )

    def build(self):

        if self.df.empty:

            fig = go.Figure()

            fig.update_layout(

                title="Weekday Activity",

                template=CURRENT_THEME["template"]

            )

            return fig

        self.df["weekday"] = self.df["event_date"].dt.day_name()

        self.df["hour"] = self.df["event_date"].dt.hour

        weekday_order = [

            "Monday",

            "Tuesday",

            "Wednesday",

            "Thursday",

            "Friday",

            "Saturday",

            "Sunday"

        ]

        heatmap = (

            self.df

            .pivot_table(

                index="weekday",

                columns="hour",

                values="integration_system",

                aggfunc="count",

                fill_value=0

            )

            .reindex(weekday_order)

        )

        hours = list(range(24))

        heatmap = heatmap.reindex(

            columns=hours,

            fill_value=0

        )

        fig = go.Figure(

            go.Heatmap(

                z=heatmap.values,

                x=hours,

                y=heatmap.index,

                colorscale=[

                    [0.00, "#F8FAFC"],

                    [0.20, "#DBEAFE"],

                    [0.40, "#93C5FD"],

                    [0.60, "#3B82F6"],

                    [0.80, "#1D4ED8"],

                    [1.00, "#1E3A8A"]

                ],

                hovertemplate=

                "<b>%{y}</b><br>"

                "Hour : %{x}:00<br>"

                "Executions : %{z}"

                "<extra></extra>",

                colorbar=dict(

                    title="Executions"

                )

            )

        )

        fig.update_layout(

            title=dict(

                text="Weekday vs Hour Execution Heatmap",

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

            )

        )

        fig.update_xaxes(

            title="Hour of Day",

            tickmode="array",

            tickvals=list(range(24)),

            ticktext=[

                f"{h:02d}:00"

                for h in range(24)

            ],

            showgrid=False

        )

        fig.update_yaxes(

            title="Weekday",

            autorange="reversed"

        )

        return fig


if __name__ == "__main__":

    from services.excel_parser import ExcelParser
    from services.data_cleaner import DataCleaner
    from services.data_merger import DataMerger

    parser = ExcelParser()

    frames = parser.load_all()

    cleaned = {

        key: DataCleaner(value).clean()

        for key, value in frames.items()

    }

    master = DataMerger(cleaned).merge()

    chart = WeekdayHeatmapChart(master)

    fig = chart.build()

    fig.show()