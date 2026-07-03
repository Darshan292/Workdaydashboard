"""
Enterprise Cache Manager
"""

from functools import wraps
from flask_caching import Cache

from config.settings import (
    CACHE_TYPE,
    CACHE_DIRECTORY,
    CACHE_THRESHOLD
)

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": str(CACHE_DIRECTORY),
        "CACHE_THRESHOLD": CACHE_THRESHOLD,
        "CACHE_DEFAULT_TIMEOUT": 900,
    }
)


def init_cache(app):
    """
    Initialize Flask Cache.
    """
    cache.init_app(app)


def cached(timeout=900):
    """
    Generic cache decorator.
    """

    def decorator(func):

        @cache.memoize(timeout=timeout)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def clear_cache():
    """
    Clear entire cache.
    """
    cache.clear()


@cached(timeout=900)
def cache_dataframe(df):
    """
    Cache dataframe reference.
    """
    return df


@cached(timeout=900)
def cache_kpis(kpi_dict):
    """
    Cache KPI calculations.
    """
    return kpi_dict


@cached(timeout=900)
def cache_chart(name, figure):
    """
    Cache plotly figures.
    """
    return figure


@cached(timeout=900)
def cache_table(df):
    """
    Cache processed table.
    """
    return df


def cache_info():

    return {
        "type": CACHE_TYPE,
        "directory": str(CACHE_DIRECTORY),
        "threshold": CACHE_THRESHOLD,
    }


if __name__ == "__main__":

    print("=" * 60)

    print("CACHE SETTINGS")

    print("=" * 60)

    for k, v in cache_info().items():
        print(f"{k:<15}: {v}")