#!/usr/bin/env python3
"""
Python function that returns all students sorted by average score
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        List of dictionaries representing students sorted by average score.
        Each dictionary includes the key 'averageScore'.
    """
    students = mongo_collection.aggregate(
        [
            {"$unwind": "$topics"},
            {
                "$group": {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "averageScore": {"$avg": "$topics.score"},
                }
            },
            {"$sort": {"averageScore": -1}},
        ]
    )

    return list(students)
