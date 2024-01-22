#!/usr/bin/env python3
"""
This script defines a function to retrieve a list of schools
having a specific topic
"""
from pymongo.collection import Collection
from typing import List


def schools_by_topic(mongo_collection: Collection,
                     topic: str) -> List[dict]:
    """
    Retrieve a list of schools having a specific topic.

    Args:
        mongo_collection: PyMongo collection object.
        topic: Topic to search.

    Returns:
        A list of dictionaries representing schools having
        the specified topic.
    """
    schools = list(mongo_collection.find({"topics": topic}))

    return schools
