"""
Enterprise KPI Callbacks
"""

import pandas as pd

from dash import Input, Output

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
            Output("kpi-runtime-arrow", "children"),
        ],
        Input("filtered-data", "data"),
    )
    def update_kpis(filtered_data):

        if not filtered_data:
            return (
                "0", "0", "0", "0",
                "0%", "0%",
                "0 s", "0 s",
                "0", "0",
                "0", "0",
                "0", "0",
                "0",
                "▬", "▬", "▬"
            )

        df = pd.DataFrame(filtered_data)

        if df.empty:
            return (
                "0", "0", "0", "0",
                "0%", "0%",
                "0 s", "0 s",
                "0", "0",
                "0", "0",
                "0", "0",
                "0",
                "▬", "▬", "▬"
            )

        engine = KPIEngine(df)

        metrics = engine.build()

        total = metrics["total_executions"]
        success = metrics["successful_executions"]
        failed = metrics["failed_executions"]
        warning = metrics["warning_executions"]

        success_rate = metrics["success_rate"]
        failure_rate = metrics["failure_rate"]

        avg_runtime = metrics["average_processing_time"]

        return (

            str(total["current"]),

            str(success["current"]),

            str(failed["current"]),

            str(warning["current"]),

            f'{success_rate["current"]:.2f}%',

            f'{failure_rate["current"]:.2f}%',

            f'{avg_runtime["current"]:.2f} s',

            f'{metrics["longest_processing_time"]["value"]:.2f} s',

            str(metrics["active_integrations"]["value"]),

            str(metrics["items_processed"]["value"]),

            str(metrics["critical_failures"]["value"]),

            "3",

            str(metrics["slow_integrations"]["value"]),

            f'{metrics["average_throughput"]["value"]:.2f}',

            str(metrics["todays_executions"]["value"]),

            success_rate["arrow"],

            failure_rate["arrow"],

            avg_runtime["arrow"]

        )