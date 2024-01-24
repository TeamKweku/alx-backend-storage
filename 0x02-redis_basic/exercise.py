#!/usr/bin/env python3
"""module that creates a Cache class"""
import redis
import uuid
from typing import Union


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
