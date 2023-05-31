from contextlib import contextmanager
from find_artists import cache


@contextmanager
def cache_manager(key):
    try:
        yield cache[key]
    finally:
        del cache[key]
