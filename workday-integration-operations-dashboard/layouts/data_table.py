"""
Enterprise Data Table
"""

from dash import html
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc


class EnterpriseDataTable:

    def __init__(self, dataframe):

        self.df = dataframe

    @staticmethod
    def conditional_styles():

        return [

            {
                "if": {
                    "filter_query": '{status} = "Failed"'
                },
                "backgroundColor": "#FEE2E2",
                "color": "#991B1B",
                "fontWeight": "600"
            },

            {
                "if": {
                    "filter_query": '{status} = "Warning"'
                },
                "backgroundColor": "#FEF3C7",
                "color": "#92400E",
                "fontWeight": "600"
            },

            {
                "if": {
                    "filter_query": '{status} = "Success"'
                },
                "backgroundColor": "#DCFCE7",
                "color": "#166534"
            },

            {
                "if": {
                    "filter_query":
                    "{processing_time_seconds} > 60"
                },
                "backgroundColor": "#FFE4E6"
            }

        ]

    def build(self):

        return dbc.Card(

            [

                dbc.CardHeader(

                    dbc.Row(

                        [

                            dbc.Col(

                                html.H5(

                                    "Integration Execution Details",

                                    className="mb-0"

                                )

                            ),

                            dbc.Col(

                                html.Div(

                                    id="table-record-count",

                                    children=f"{len(self.df):,} Records",

                                    className="record-counter"

                                ),

                                width="auto"

                            ),

                            dbc.Col(

                                dbc.Button(

                                    [

                                        html.I(

                                            className="fa-solid fa-download me-2"

                                        ),

                                        "Export"

                                    ],

                                    id="export-table",

                                    color="primary",

                                    className="export-button"

                                ),

                                width="auto"

                            )

                        ],

                        align="center",

                        justify="between"

                    )

                ),

                dbc.CardBody(

                    [

                        dash_table.DataTable(

                            id="integration-table",

                            columns=[

                                {

                                    "name": c.replace(

                                        "_",

                                        " "

                                    ).title(),

                                    "id": c

                                }

                                for c in self.df.columns

                            ],

                            data=self.df.to_dict(

                                "records"

                            ),

                            page_size=25,

                            page_action="native",

                            filter_action="native",

                            sort_action="native",

                            sort_mode="multi",

                            row_selectable="single",

                            editable=False,

                            export_format="none",

                            fixed_rows={

                                "headers": True

                            },

                            style_table={

                                "height":"700px",

                                "overflowY":"auto",

                                "overflowX":"auto"

                            },

                            style_header={

                                "backgroundColor":"#0F172A",

                                "color":"white",

                                "fontWeight":"bold",

                                "textAlign":"center"

                            },

                            style_cell={

                                "padding":"10px",

                                "fontSize":"13px",

                                "textAlign":"left",

                                "minWidth":"150px",

                                "width":"150px",

                                "maxWidth":"350px",

                                "whiteSpace":"normal"

                            },

                            style_data_conditional=self.conditional_styles()

                        )

                    ]

                )

            ],

            className="dashboard-card"

        )