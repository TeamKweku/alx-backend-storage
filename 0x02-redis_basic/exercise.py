#!/usr/bin/env python3
"""module that creates a Cache class"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    def __init__(self) -> None:
        """
        Initialize the Cache object with a Redis client and flush the database.

        The Redis client instance is stored as a private variable named _redis,
        and the flushdb method is called to clear the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
