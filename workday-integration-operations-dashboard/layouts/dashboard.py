"""
Enterprise Dashboard Root Layout
"""

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from layouts.header import build_header
from layouts.sidebar import build_sidebar
from layouts.kpi_cards import build_kpi_cards
from layouts.chart_grid import ChartGrid
from layouts.data_table import EnterpriseDataTable
# from layouts.footer import build_footer


class DashboardLayout:

    def __init__(self, dataframe):

        self.df = dataframe

    def build(self):

        return html.Div(

            id="dashboard-root",

            className="dashboard-root dark-theme",

            children=[

                # =====================================================
                # STORES
                # =====================================================

                dcc.Store(
                    id="master-data",
                    data=self.df.to_dict("records")
                ),

                dcc.Store(
                    id="filtered-data",
                    data=self.df.to_dict("records")
                ),

                dcc.Store(
                    id="theme-store",
                    data="dark"
                ),

                dcc.Store(
                    id="theme-persistence",
                    storage_type="local"
                ),

                dcc.Store(
                    id="sidebar-state",
                    data=False
                ),

                # =====================================================
                # DOWNLOAD
                # =====================================================

                dcc.Download(
                    id="download-dataframe"
                ),

                # =====================================================
                # AUTO REFRESH
                # =====================================================

                dcc.Interval(

                    id="auto-refresh",

                    interval=60000,

                    n_intervals=0

                ),

                # =====================================================
                # LOADING
                # =====================================================

                dcc.Loading(

                    id="dashboard-loading",

                    type="circle",

                    #fullscreen=True,

                    children=[

                        dbc.Container(

                            [

                                build_header(),

                                dbc.Row(

                                    [

                                        dbc.Col(

                                            html.Div(

                                                build_sidebar(),

                                                id="sidebar-container"

                                            ),

                                            xl=2,

                                            lg=3,

                                            md=12

                                        ),

                                        dbc.Col(

                                            [

                                                build_kpi_cards(),

                                                html.Br(),

                                                ChartGrid(

                                                    self.df

                                                ).build(),

                                                html.Br(),

                                                EnterpriseDataTable(

                                                    self.df

                                                ).build(),

                                                html.Br(),

                                                # build_footer()

                                            ],

                                            xl=10,

                                            lg=9,

                                            md=12

                                        )

                                    ],

                                    className="g-4"

                                )

                            ],

                            fluid=True,

                            className="dashboard-container"

                        )

                    ]

                ),

                # =====================================================
                # TOAST
                # =====================================================

                dbc.Toast(

                    id="notification-toast",

                    header="Notification",

                    icon="primary",

                    dismissable=True,

                    is_open=False,

                    duration=4000,

                    style={

                        "position":"fixed",

                        "top":"20px",

                        "right":"20px",

                        "width":"360px",

                        "zIndex":9999

                    }

                )

            ]

        )

    # def build(self):

    #     return html.Div(

    #         [

    #             html.H1("Dashboard Works"),

    #             dcc.Store(
    #                 id="master-data",
    #                 data=self.df.to_dict("records")
    #             ),

    #             dcc.Store(
    #                 id="filtered-data",
    #                 data=self.df.to_dict("records")
    #             ),

    #             build_header(),
    #             build_sidebar(),
    #             build_kpi_cards(),
    #             ChartGrid(self.df).build()
                

    #         ]

    #     )