"""
Enterprise Failure Sankey Diagram
"""

import pandas as pd
import plotly.graph_objects as go

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME


class FailureSankeyChart(BaseChart):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    def build(self):

        if self.df.empty:

            return self.empty_figure(
                "Failure Flow Analysis"
            )

        failures = self.df[

            self.df["status"] == "Failed"

        ].copy()

        if failures.empty:

            return self.empty_figure(
                "Failure Flow Analysis"
            )

        failures["failure_reason"] = (

            failures["errors_warnings"]

            .fillna("Unknown Error")

            .replace("", "Unknown Error")

        )

        failures["response"] = (

            failures["response_message"]

            .fillna("No Response")

            .replace("", "No Response")

            .astype(str)

            .str.slice(0, 45)

        )

        failures["status"] = (

            failures["status"]

            .fillna("Unknown")

        )

        # =====================================================
        # Nodes
        # =====================================================

        node_map = {}

        labels = []

        colors = []

        def add_node(name, color):

            if name not in node_map:

                node_map[name] = len(labels)

                labels.append(name)

                colors.append(color)

            return node_map[name]

        # =====================================================
        # Create Nodes
        # =====================================================

        for _, row in failures.iterrows():

            add_node(

                row["integration_system"],

                CURRENT_THEME["primary"]

            )

            add_node(

                row["failure_reason"],

                CURRENT_THEME["danger"]

            )

            add_node(

                row["response"],

                CURRENT_THEME["warning"]

            )

            add_node(

                row["status"],

                CURRENT_THEME["secondary"]

            )

        # =====================================================
        # Links
        # =====================================================

        flow = {}

        def add_link(source, target):

            key = (source, target)

            flow[key] = flow.get(key, 0) + 1

        for _, row in failures.iterrows():

            integration = row["integration_system"]

            reason = row["failure_reason"]

            response = row["response"]

            status = row["status"]

            add_link(integration, reason)

            add_link(reason, response)

            add_link(response, status)

        source = []

        target = []

        value = []

        link_colors = []

        for (s, t), count in flow.items():

            source.append(

                node_map[s]

            )

            target.append(

                node_map[t]

            )

            value.append(

                count

            )

            link_colors.append(

                "rgba(239,68,68,0.30)"

            )

        fig = go.Figure(

            go.Sankey(

                arrangement="snap",

                node=dict(

                    pad=22,

                    thickness=20,

                    line=dict(

                        color="white",

                        width=1

                    ),

                    label=labels,

                    color=colors,

                    hovertemplate=

                    "<b>%{label}</b>"

                    "<extra></extra>"

                ),

                link=dict(

                    source=source,

                    target=target,

                    value=value,

                    color=link_colors,

                    hovertemplate=

                    "Flow : %{value}"

                    "<extra></extra>"

                )

            )

        )

        self.apply_layout(

            fig,

            "Failure Flow Analysis",

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

    chart = FailureSankeyChart(master)

    fig = chart.build()

    fig.show(config=chart.config())