"""
=========================================================
Workday Integration Operations Dashboard
Application Configuration
=========================================================
"""

from pathlib import Path
from datetime import timedelta


# -------------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"


# -------------------------------------------------------
# EXCEL FILES
# -------------------------------------------------------

FAILURE_REPORT = DATA_DIR / "CR Integrations Failure in past 7 days.xlsx"

EVENT_STATISTICS_REPORT = (
    DATA_DIR / "CR Integrations Event Statistics Data in past 7 days.xlsx"
)

PROCESSING_TIME_REPORT = (
    DATA_DIR / "CR integrations with higher processing time in past 7 days.xlsx"
)


EXCEL_FILES = [
    FAILURE_REPORT,
    EVENT_STATISTICS_REPORT,
    PROCESSING_TIME_REPORT,
]


# -------------------------------------------------------
# APPLICATION
# -------------------------------------------------------

APP_NAME = "Workday Integration Operations Center"

APP_VERSION = "1.0.0"

COMPANY = "Enterprise Dashboard"

DEFAULT_TIMEZONE = "Asia/Kolkata"

AUTO_REFRESH_INTERVAL = 60  # seconds

CACHE_TIMEOUT = timedelta(minutes=15)


# -------------------------------------------------------
# PERFORMANCE
# -------------------------------------------------------

MAX_UPLOAD_ROWS = 1_000_000

DEFAULT_PAGE_SIZE = 25

MAX_TABLE_ROWS = 5000

MAX_WORDCLOUD_WORDS = 200

TREND_LOOKBACK_DAYS = 7


# -------------------------------------------------------
# DATE FORMATS
# -------------------------------------------------------

DATE_FORMAT = "%d-%m-%Y"

TIME_FORMAT = "%H:%M:%S"

DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"


# -------------------------------------------------------
# KPI TARGETS
# -------------------------------------------------------

SUCCESS_TARGET = 99.0

FAILURE_TARGET = 1.0

PROCESSING_TIME_TARGET = 30

HEALTH_SCORE_TARGET = 95


# -------------------------------------------------------
# DASHBOARD SETTINGS
# -------------------------------------------------------

DEFAULT_THEME = "light"

DEFAULT_TEMPLATE = "plotly_white"

DEFAULT_FONT = "Inter"

ENABLE_ANIMATIONS = True

ENABLE_CACHE = True

ENABLE_AUTO_REFRESH = True

SHOW_LOADING_SPINNER = True

ENABLE_TOASTS = True


# -------------------------------------------------------
# CHART SETTINGS
# -------------------------------------------------------

DEFAULT_HEIGHT = 360

LARGE_CHART_HEIGHT = 480

SMALL_CHART_HEIGHT = 250

CHART_MARGIN = dict(
    l=20,
    r=20,
    t=40,
    b=20
)


# -------------------------------------------------------
# FILTER DEFAULTS
# -------------------------------------------------------

DEFAULT_PERIOD = "Last 7 Days"

DEFAULT_STATUS = "All"

DEFAULT_REPORT = "All"

DEFAULT_INTEGRATION = "All"


# -------------------------------------------------------
# TABLE SETTINGS
# -------------------------------------------------------

TABLE_PAGE_SIZE = 20

TABLE_EXPORT_FORMAT = "xlsx"

TABLE_FILTER_CASE = "insensitive"

ENABLE_ROW_SELECTION = True


# -------------------------------------------------------
# CACHE SETTINGS
# -------------------------------------------------------

CACHE_TYPE = "disk"

CACHE_DIRECTORY = CACHE_DIR

CACHE_THRESHOLD = 500


# -------------------------------------------------------
# LOGGING
# -------------------------------------------------------

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "dashboard.log"


# -------------------------------------------------------
# STATUS COLORS
# -------------------------------------------------------

STATUS_ORDER = [
    "Success",
    "Warning",
    "Failed",
    "Running",
    "Cancelled",
]

STATUS_PRIORITY = {
    "Failed": 1,
    "Warning": 2,
    "Running": 3,
    "Success": 4,
    "Cancelled": 5,
}


# -------------------------------------------------------
# FILE VALIDATION
# -------------------------------------------------------

SUPPORTED_EXTENSIONS = [
    ".xlsx",
    ".xls",
]


# -------------------------------------------------------
# APP METADATA
# -------------------------------------------------------

APP_DESCRIPTION = """
Enterprise monitoring platform for
Workday Integration Operations.
"""

AUTHOR = "Darshan"

COPYRIGHT = "© 2026"