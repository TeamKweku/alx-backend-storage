#!/usr/bin/env python3
"""
This script defines a function to update the topics of
a school document based on the school name
"""
from pymongo.collection import Collection
from typing import List


def update_topics(mongo_collection: Collection,
                  name: str, topics: List[str]) -> None:
    """
    Update the topics of a school document based on the school name.

    Args:
        mongo_collection: PyMongo collection object.
        name: School name to update.
        topics: List of strings representing the new topics.

    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
