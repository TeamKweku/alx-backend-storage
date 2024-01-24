#!/usr/bin/env python3
"""module that creates a Cache class"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """
    counts how many times methods of Cache class are called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    tracks the call history of a method in a Cache classs.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output."""
        in_key = "{}:inputs".format(method.__qualname__)
        out_key = "{}:outputs".format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output

    return wrapper


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method."""
    if fn is None or not hasattr(fn, "__self__"):
        return
    redis_store = getattr(fn.__self__, "_redis", None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = "{}:inputs".format(fxn_name)
    out_key = "{}:outputs".format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print("{} was called {} times:".format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print(
            "{}(*{}) -> {}".format(
                fxn_name,
                fxn_input.decode("utf-8"),
                fxn_output,
            )
        )


class Cache:
    def __init__(self) -> None:
        """
        Initialize the Cache object with a Redis client and flush the database.

        The Redis client instance is stored as a private variable named _redis,
        and the flushdb method is called to clear the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in
            Redis.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves data from redis using the provided key

        Args:
            key (str): key to retrieve value

        Returns:
            returns: (str or None)
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage

        Args:
            key (str): key to retrieve value

        Return:
            returns (str): value
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage

        Args:
            key (str): key to retrieve value

        Return:
            returns (int): value
        """
        return self.get(key, lambda x: int(x))
