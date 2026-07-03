"""
Application Constants
"""

from dash import dcc

# ==========================================================
# DASHBOARD
# ==========================================================

APP_TITLE = "Workday Integration Operations Center"

APP_SUBTITLE = (
    "Enterprise Monitoring & Analytics Dashboard"
)

# ==========================================================
# REFRESH
# ==========================================================

AUTO_REFRESH_INTERVAL = 60 * 1000  # milliseconds

REFRESH_COMPONENT = dcc.Interval(
    id="auto-refresh",
    interval=AUTO_REFRESH_INTERVAL,
    n_intervals=0
)

# ==========================================================
# THEMES
# ==========================================================

LIGHT_THEME = "light"

DARK_THEME = "dark"

# ==========================================================
# KPI CARDS
# ==========================================================

KPI_CARDS = [

    "Total Executions",

    "Successful Executions",

    "Failed Executions",

    "Warning Executions",

    "Success Rate",

    "Failure Rate",

    "Average Processing Time",

    "Longest Processing Time",

    "Active Integrations",

    "Total Items Processed",

    "Critical Failures",

    "Processing Reports",

    "Slow Integrations",

    "Average Throughput",

    "Today's Executions"

]

# ==========================================================
# STATUS
# ==========================================================

STATUS_SUCCESS = "Success"

STATUS_FAILED = "Failed"

STATUS_WARNING = "Warning"

STATUS_RUNNING = "Running"

STATUS_CANCELLED = "Cancelled"

STATUS_LIST = [

    STATUS_SUCCESS,

    STATUS_FAILED,

    STATUS_WARNING,

    STATUS_RUNNING,

    STATUS_CANCELLED

]

# ==========================================================
# FILTER OPTIONS
# ==========================================================

TIME_OPTIONS = [

    "Today",

    "Yesterday",

    "Last 7 Days",

    "Last 30 Days",

    "This Month",

    "Custom"

]

REPORT_TYPES = [

    "Failures",

    "Event Statistics",

    "Processing Time"

]

# ==========================================================
# TABLE
# ==========================================================

TABLE_PAGE_SIZE = 20

TABLE_PAGE_OPTIONS = [

    20,

    50,

    100,

    250

]

# ==========================================================
# CHART IDS
# ==========================================================

CHART_IDS = {

    "trend": "execution-trend",

    "status": "status-distribution",

    "calendar": "calendar-heatmap",

    "weekday": "weekday-heatmap",

    "hourly": "hourly-trend",

    "weekly": "weekly-area",

    "monthly": "monthly-area",

    "top": "top-integrations",

    "slow": "slow-integrations",

    "runtime": "runtime-distribution",

    "outliers": "runtime-outliers",

    "timeline": "processing-timeline",

    "failure": "failure-trend",

    "treemap": "failure-treemap",

    "sunburst": "failure-sunburst",

    "sankey": "failure-sankey",

    "wordcloud": "error-wordcloud",

    "health": "integration-health",

    "gauge": "health-gauge",

    "waterfall": "execution-waterfall",

    "items": "items-treemap",

    "violin": "processing-violin",

    "stacked": "success-failure",

    "ranking": "integration-ranking",

    "trend_rank": "trend-ranking",

    "activity": "live-activity",

    "table": "integration-table"

}

# ==========================================================
# DEFAULT ANIMATION
# ==========================================================

TRANSITION_DURATION = 600

EASING = "cubic-in-out"

# ==========================================================
# BOOTSTRAP ICONS
# ==========================================================

ICONS = {

    "success": "bi bi-check-circle-fill",

    "failed": "bi bi-x-circle-fill",

    "warning": "bi bi-exclamation-triangle-fill",

    "runtime": "bi bi-clock-history",

    "items": "bi bi-box-seam",

    "integration": "bi bi-diagram-3-fill",

    "refresh": "bi bi-arrow-repeat",

    "calendar": "bi bi-calendar3",

    "trend_up": "bi bi-arrow-up-right",

    "trend_down": "bi bi-arrow-down-right",

    "search": "bi bi-search",

    "filter": "bi bi-funnel-fill",

    "dashboard": "bi bi-speedometer2",

    "table": "bi bi-table",

    "download": "bi bi-download",

    "theme": "bi bi-moon-stars-fill"

}