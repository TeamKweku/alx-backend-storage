#!/usr/bin/env python3
"""
This script defines a function to list all documents
in a given MongoDB collection
"""
from typing import List


def list_all(mongo_collection) -> List[dict]:
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        A list of all documents in the collection.
        Returns an empty list if no documents are found.
    """
    documents = list(mongo_collection.find())

    return documents
