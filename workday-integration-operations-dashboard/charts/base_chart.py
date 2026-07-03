"""
Enterprise Base Chart
Shared styling for all dashboard charts.
"""

import plotly.graph_objects as go

from config.theme import CURRENT_THEME


class BaseChart:

    def __init__(self):

        self.theme = CURRENT_THEME

    # =====================================================
    # Empty Figure
    # =====================================================

    def empty_figure(self, title):

        fig = go.Figure()

        fig.update_layout(

            title=title,

            template=self.theme["template"],

            paper_bgcolor=self.theme["paper"],

            plot_bgcolor=self.theme["paper"],

            height=420,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )

        )

        fig.add_annotation(

            text="No Data Available",

            showarrow=False,

            font=dict(
                size=18,
                color=self.theme["secondary_text"]
            )

        )

        return fig

    # =====================================================
    # Apply Enterprise Layout
    # =====================================================

    def apply_layout(

        self,

        fig,

        title,

        height=420,

        legend=True

    ):

        fig.update_layout(

            title=dict(

                text=title,

                x=0.02,

                font=dict(
                    size=20
                )

            ),

            template=self.theme["template"],

            paper_bgcolor=self.theme["paper"],

            plot_bgcolor=self.theme["paper"],

            font=dict(

                family="Inter",

                color=self.theme["text"]

            ),

            hovermode="x unified",

            height=height,

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

            showlegend=legend

        )

        return fig

    # =====================================================
    # Standard X Axis
    # =====================================================

    def style_xaxis(

        self,

        fig,

        title=""

    ):

        fig.update_xaxes(

            title=title,

            showgrid=False,

            zeroline=False

        )

    # =====================================================
    # Standard Y Axis
    # =====================================================

    def style_yaxis(

        self,

        fig,

        title=""

    ):

        fig.update_yaxes(

            title=title,

            gridcolor=self.theme["grid"],

            zeroline=False

        )

    # =====================================================
    # Standard Modebar
    # =====================================================

    @staticmethod
    def config():

        return {

            "displaylogo": False,

            "responsive": True,

            "scrollZoom": True,

            "toImageButtonOptions": {

                "format": "png",

                "filename": "workday_dashboard"

            },

            "modeBarButtonsToRemove": [

                "lasso2d",

                "select2d",

                "autoScale2d"

            ]

        }