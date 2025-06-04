from functools import wraps
import sqlite3
import logging


def handle_db_errors(message="Error message is not specified"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.Error as e:
                logging.error(message)
                logging.error(f"An error occurred in {func.__name__}: {e}")
                
        return wrapper
    return decorator