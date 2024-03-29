#!/usr/bin/env python3
"""
This script provides statistics about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def print_log_stats(collection):
    """
    Display statistics about Nginx logs in MongoDB
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    # Total logs
    total_logs: int = collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods statistics
    print("Methods:")
    for method in methods:
        method_count: int = \
            collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Status check count
    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"}
        )
    print(f"{status_check_count} status check")


def trigger_logs() -> None:
    """
    Function that connects to the MongoDB client and triggers function
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx
    print_log_stats(log_collection)


if __name__ == "__main__":
    """main function call"""
    trigger_logs()
