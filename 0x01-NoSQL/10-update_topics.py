#!/usr/bin/env python3
"""
This script defines a function to update the topics of
a school document based on the school name
"""


def update_topics(mongo_collection, name, topics):
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
