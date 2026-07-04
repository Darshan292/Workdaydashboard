"""
Enterprise KPI Callbacks
"""

import pandas as pd

from dash import Input
from dash import Output

from services.kpi_engine import KPIEngine


def register_kpi_callbacks(app):

    @app.callback(

        [

            Output("kpi-total-executions", "children"),
            Output("kpi-successful-executions", "children"),
            Output("kpi-failed-executions", "children"),
            Output("kpi-warning-executions", "children"),

            Output("kpi-success-rate", "children"),
            Output("kpi-failure-rate", "children"),

            Output("kpi-average-runtime", "children"),
            Output("kpi-longest-runtime", "children"),

            Output("kpi-active-integrations", "children"),
            Output("kpi-total-items", "children"),

            Output("kpi-critical-failures", "children"),
            Output("kpi-processing-reports", "children"),

            Output("kpi-slow-integrations", "children"),
            Output("kpi-throughput", "children"),
            Output("kpi-today-executions", "children"),

            Output("kpi-success-arrow", "children"),
            Output("kpi-failure-arrow", "children"),
            Output("kpi-runtime-arrow", "children")

        ],

        Input(

            "filtered-data",

            "data"

        )

    )

    def update_kpis(

        filtered_data

    ):

        if filtered_data is None:

            df = pd.DataFrame()

        else:

            df = pd.DataFrame(

                filtered_data

            )

        if df.empty:

            return (

                "0",

                "0",

                "0",

                "0",

                "0%",

                "0%",

                "0 s",

                "0 s",

                "0",

                "0",

                "0",

                "0",

                "0",

                "0",

                "0",

                "►",

                "►",

                "►"

            )

        engine = KPIEngine(

            df

        )

        metrics = engine.calculate()

        success_arrow = (

            "▲"

            if metrics["success_rate"] >= 95

            else

            "▼"

        )

        failure_arrow = (

            "▲"

            if metrics["failure_rate"] > 5

            else

            "▼"

        )

        runtime_arrow = (

            "▲"

            if metrics["average_processing_time"] > 30

            else

            "▼"

        )

        return (

            f"{metrics['total_executions']:,}",

            f"{metrics['successful_executions']:,}",

            f"{metrics['failed_executions']:,}",

            f"{metrics['warning_executions']:,}",

            f"{metrics['success_rate']:.2f}%",

            f"{metrics['failure_rate']:.2f}%",

            f"{metrics['average_processing_time']:.2f} s",

            f"{metrics['longest_processing_time']:.2f} s",

            f"{metrics['active_integrations']:,}",

            f"{metrics['total_items_processed']:,}",

            f"{metrics['critical_failures']:,}",

            f"{metrics['processing_reports']:,}",

            f"{metrics['slow_integrations']:,}",

            f"{metrics['average_throughput']:.2f}",

            f"{metrics['today_executions']:,}",

            success_arrow,

            failure_arrow,

            runtime_arrow

        )