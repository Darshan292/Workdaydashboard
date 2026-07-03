"""
Enterprise Health Gauge Dashboard
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from charts.base_chart import BaseChart


class HealthGaugeChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # ============================================================
    # Calculate Scores
    # ============================================================

    def calculate(self):

        grouped = (

            self.df

            .groupby("integration_system")

            .agg(

                executions=("integration_system", "count"),

                success=("is_success", "sum"),

                failures=("is_failed", "sum"),

                runtime=("processing_time_seconds", "mean")

            )

            .reset_index()

        )

        grouped["health"] = (

            (

                grouped["success"]

                /

                grouped["executions"]

            )

            * 100

        )

        grouped["health"] = (

            grouped["health"]

            -

            grouped["runtime"] * 0.15

        )

        grouped["health"] = (

            grouped["health"]

            .clip(

                lower=0,

                upper=100

            )

            .round(1)

        )

        return grouped.sort_values(

            "health",

            ascending=False

        )

    # ============================================================
    # Build
    # ============================================================

    def build(self, top_n=6):

        if self.df.empty:

            return self.empty_figure(

                "Integration Health"

            )

        health = self.calculate().head(top_n)

        rows = 2

        cols = 3

        fig = make_subplots(

            rows=rows,

            cols=cols,

            specs=[

                [

                    {"type": "indicator"},

                    {"type": "indicator"},

                    {"type": "indicator"}

                ],

                [

                    {"type": "indicator"},

                    {"type": "indicator"},

                    {"type": "indicator"}

                ]

            ],

            subplot_titles=list(

                health["integration_system"]

            )

        )

        row = 1

        col = 1

        for _, record in health.iterrows():

            fig.add_trace(

                go.Indicator(

                    mode="gauge+number",

                    value=record["health"],

                    number={

                        "suffix": "%"

                    },

                    gauge={

                        "axis": {

                            "range": [0, 100]

                        },

                        "bar": {

                            "thickness": 0.45

                        },

                        "steps": [

                            {

                                "range": [0, 50],

                                "color": "#DC2626"

                            },

                            {

                                "range": [50, 75],

                                "color": "#FACC15"

                            },

                            {

                                "range": [75, 90],

                                "color": "#60A5FA"

                            },

                            {

                                "range": [90, 100],

                                "color": "#22C55E"

                            }

                        ],

                        "threshold": {

                            "line": {

                                "color": "black",

                                "width": 3

                            },

                            "value": record["health"]

                        }

                    }

                ),

                row=row,

                col=col

            )

            col += 1

            if col > cols:

                row += 1

                col = 1

        self.apply_layout(

            fig,

            "Integration Health Gauges",

            height=650,

            legend=False

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

    chart = HealthGaugeChart(master)

    fig = chart.build()

    fig.show(config=chart.config())