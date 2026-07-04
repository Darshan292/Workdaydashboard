"""
Enterprise Error Word Cloud
"""

import re
from collections import Counter

import plotly.graph_objects as go
from wordcloud import WordCloud

from charts.base_chart import BaseChart
from config.theme import CURRENT_THEME

from PIL import Image

class ErrorWordCloudChart(BaseChart):

    STOP_WORDS = {

        "the","and","for","from","with","this","that","have","has",
        "was","were","will","into","your","their","there","error",
        "message","messages","warning","warnings","response",
        "integration","event","workday","process","processing",
        "request","failed","failure","null","none","cannot",
        "could","would","should","exception","system","file",
        "operation","info","status","result","returned","received"
    }

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe.copy()

    # =====================================================
    # Prepare Text
    # =====================================================

    def build_text(self):

        columns = [

            "errors_warnings",

            "messages",

            "response_message"

        ]

        text = []

        for col in columns:

            if col in self.df.columns:

                text.extend(

                    self.df[col]

                    .fillna("")

                    .astype(str)

                    .tolist()

                )

        return " ".join(text)

    # =====================================================
    # Top Keywords
    # =====================================================

    def keyword_frequency(self, text):

        words = re.findall(

            r"[A-Za-z]{3,}",

            text.lower()

        )

        words = [

            w

            for w in words

            if w not in self.STOP_WORDS

        ]

        return Counter(words)

    # =====================================================
    # Build Figure
    # =====================================================

    def build(self):

        if self.df.empty:

            return self.empty_figure(

                "Error Keyword Analysis"

            )

        text = self.build_text()

        frequencies = self.keyword_frequency(text)

        if len(frequencies) == 0:

            return self.empty_figure(

                "Error Keyword Analysis"

            )

        wc = WordCloud(

            width=900,

            height=450,

            background_color="white",

            max_words=120,

            collocations=False

        )

        wc.generate_from_frequencies(
            frequencies
        )

        image = wc.to_image()

        fig = go.Figure()

        fig.add_layout_image(

            dict(

                source=image,

                x=0,

                y=1,

                sizex=1,

                sizey=1,

                xref="paper",

                yref="paper",

                sizing="stretch",

                layer="below"

            )

        )

        self.apply_layout(

            fig,

            "Error Keyword Analysis",

            height=520,

            legend=False

        )

        fig.update_xaxes(

            visible=False

        )

        fig.update_yaxes(

            visible=False

        )

        return fig

    # =====================================================
    # Top Keywords Table
    # =====================================================

    def top_keywords(

        self,

        top_n=20

    ):

        text = self.build_text()

        freq = self.keyword_frequency(text)

        return freq.most_common(top_n)

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

    chart = ErrorWordCloudChart(master)

    fig = chart.build()

    fig.show(config=chart.config())

    print(chart.top_keywords())