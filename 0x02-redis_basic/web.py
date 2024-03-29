#!/usr/bin/env python3
"""A module that implements a function that caches the number of times
a url is visited
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data of the
    provided url
    """

    @wraps(method)
    def wrapper(url) -> str:
        """The wrapper function for caching the output."""
        redis_store.incr(f"count:{url}")
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, result)
        return result

    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return requests.get(url).text
