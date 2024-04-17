"""Utility module"""

import base64
import logging
from functools import wraps

import pymysql

logger = logging.getLogger(__name__)


def ensure_database_exists(host, user, password, database_name):
    """
    Decorator that ensures a MySQL database exists before executing a function.

    Args:
        host (str): The host address of the MySQL server.
        user (str): The username for connecting to the MySQL server.
        password (str): The password for connecting to the MySQL server.
        database_name (str): The name of the database to ensure existence.

    Returns:
        function: Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with pymysql.connect(
                    host=host, user=user, password=password
                ) as connection:
                    with connection.cursor() as cursor:
                        sql = "CREATE DATABASE IF NOT EXISTS %s"
                        cursor.execute(sql, (database_name))

                logger.info(
                    "Database %s created successfully (if it didn't exist)",
                    database_name,
                )
            except pymysql.Error as error:
                logger.error("Failed to create database: %s", error)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def create_tables(models, db):
    """
    Creates tables for the given models if they don't exist in the specified database.

    Args:
        models: A list of Peewee Model instances.
        db: The database instance to create the tables in.
    """
    models_to_create = [
        # pylint: disable=W0212
        model
        for model in models
        if not db.table_exists(model._meta.table_name)
    ]
    if models_to_create:
        db.create_tables(models_to_create)


def generate_eid(username: str, msisdn: str) -> str:
    """
    Generate an entity identifier (EID) by concatenating the username and MSISDN
    and then base64 encoding the concatenated string.

    Args:
        username (str): The username of the user.
        msisdn (str): The MSISDN (mobile number) of the user.

    Returns:
        str: The base64 encoded EID.
    """
    concatenated_str = username + msisdn
    encoded_eid = base64.b64encode(concatenated_str.encode()).decode()
    return encoded_eid
