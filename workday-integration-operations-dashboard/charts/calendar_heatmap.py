"""
Enterprise Calendar Heatmap
"""

import pandas as pd
import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class CalendarHeatmapChart:

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
                title="Execution Calendar",
                template=CURRENT_THEME["template"]
            )

            return fig

        daily = (

            self.df

            .groupby(

                self.df["event_date"].dt.date

            )

            .size()

            .reset_index(name="executions")

        )

        daily.columns = [

            "date",

            "executions"

        ]

        daily["date"] = pd.to_datetime(

            daily["date"]

        )

        daily["week"] = (

            daily["date"]

            .dt.isocalendar()

            .week

            .astype(int)

        )

        daily["weekday"] = (

            daily["date"]

            .dt.weekday

        )

        weekday_labels = [

            "Mon",

            "Tue",

            "Wed",

            "Thu",

            "Fri",

            "Sat",

            "Sun"

        ]

        heatmap = daily.pivot_table(

            index="weekday",

            columns="week",

            values="executions",

            fill_value=0

        )

        fig = go.Figure(

            go.Heatmap(

                z=heatmap.values,

                x=heatmap.columns,

                y=weekday_labels,

                colorscale=[

                    [0, "#E8F1FB"],

                    [0.20, "#B8D8FF"],

                    [0.40, "#6FB5FF"],

                    [0.60, "#2E8CFF"],

                    [0.80, "#0068D9"],

                    [1.00, "#003D82"]

                ],

                colorbar=dict(

                    title="Executions"

                ),

                hovertemplate=

                "<b>Week %{x}</b><br>"

                "%{y}<br>"

                "Executions: %{z}"

                "<extra></extra>"

            )

        )

        fig.update_layout(

            title=dict(

                text="Execution Calendar",

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

            title="Week Number",

            showgrid=False

        )

        fig.update_yaxes(

            title="Day",

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

        k: DataCleaner(v).clean()

        for k, v in frames.items()

    }

    master = DataMerger(cleaned).merge()

    chart = CalendarHeatmapChart(master)

    fig = chart.build()

    fig.show()