"""
Enterprise Dashboard Theme Configuration
"""

# ===============================
# LIGHT THEME
# ===============================

LIGHT = {

    "name": "light",

    "template": "plotly_white",

    "background": "#F5F7FB",

    "paper": "#FFFFFF",

    "card": "#FFFFFF",

    "sidebar": "#FFFFFF",

    "header": "#FFFFFF",

    "text": "#202124",

    "secondary_text": "#5F6368",

    "border": "#E5E7EB",

    "grid": "#ECEFF4",

    "shadow": "0 8px 25px rgba(0,0,0,0.08)",

    "primary": "#2563EB",

    "secondary": "#0EA5E9",

    "success": "#16A34A",

    "warning": "#F59E0B",

    "danger": "#DC2626",

    "info": "#06B6D4",

    "purple": "#7C3AED",

    "pink": "#DB2777",

    "teal": "#14B8A6",

    "orange": "#EA580C",

    "gradient": [

        "#2563EB",

        "#0EA5E9",

        "#14B8A6",

        "#16A34A",

        "#F59E0B",

        "#DC2626"

    ]
}

# ===============================
# DARK THEME
# ===============================

DARK = {

    "name": "dark",

    "template": "plotly_dark",

    "background": "#0F172A",

    "paper": "#111827",

    "card": "#1E293B",

    "sidebar": "#111827",

    "header": "#111827",

    "text": "#F8FAFC",

    "secondary_text": "#CBD5E1",

    "border": "#334155",

    "grid": "#334155",

    "shadow": "0 8px 30px rgba(0,0,0,0.45)",

    "primary": "#3B82F6",

    "secondary": "#38BDF8",

    "success": "#22C55E",

    "warning": "#FBBF24",

    "danger": "#EF4444",

    "info": "#06B6D4",

    "purple": "#8B5CF6",

    "pink": "#EC4899",

    "teal": "#2DD4BF",

    "orange": "#FB923C",

    "gradient": [

        "#3B82F6",

        "#38BDF8",

        "#2DD4BF",

        "#22C55E",

        "#FBBF24",

        "#EF4444"

    ]
}

# ===============================
# TYPOGRAPHY
# ===============================

FONT_FAMILY = "Inter"

FONT_SIZE = {

    "title": 28,

    "subtitle": 20,

    "card_title": 14,

    "kpi": 34,

    "axis": 12,

    "table": 13,

    "legend": 12,

    "small": 11

}

# ===============================
# CARD SETTINGS
# ===============================

CARD = {

    "radius": "18px",

    "padding": "18px",

    "transition": "all .30s ease",

    "hover_scale": "scale(1.02)"

}

# ===============================
# GRAPH SETTINGS
# ===============================

GRAPH = {

    "height": 360,

    "radius": 18,

    "animation": 700,

    "margin": {

        "l": 20,

        "r": 20,

        "t": 50,

        "b": 20

    }

}

# ===============================
# KPI COLORS
# ===============================

KPI_COLORS = {

    "success_rate": "#16A34A",

    "failure_rate": "#DC2626",

    "processing_time": "#F59E0B",

    "throughput": "#2563EB",

    "items": "#7C3AED",

    "health": "#14B8A6"

}

# ===============================
# STATUS COLORS
# ===============================

STATUS_COLORS = {

    "Success": "#16A34A",

    "Failed": "#DC2626",

    "Warning": "#F59E0B",

    "Running": "#2563EB",

    "Cancelled": "#6B7280"

}

# ===============================
# DEFAULT
# ===============================

CURRENT_THEME = LIGHT