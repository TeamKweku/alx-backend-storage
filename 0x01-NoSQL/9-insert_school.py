#!/usr/bin/env python3
"""
This script defines a function to insert a new document
in a MongoDB collection based on kwargs
"""
from bson.objectid import ObjectId


def insert_school(mongo_collection, **kwargs) -> ObjectId:
    """
    Insert a new document into a MongoDB collection based on kwargs.

    Args:
        mongo_collection: PyMongo collection object.
        **kwargs: Keyword arguments representing the fields and values for the new document.

    Returns:
        The new _id of the inserted document.
    """
    doc_id = mongo_collection.insert_one(kwargs)
    return doc_id.inserted_id
