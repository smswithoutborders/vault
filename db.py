"""Module for connecting to a database."""

import os
import logging
from peewee import MySQLDatabase, SqliteDatabase, DatabaseError
from utils import ensure_database_exists

from config import MYSQL_HOST, MYSQL_DB_NAME, MYSQL_PASSWORD, MYSQL_USER, SQLITE_FILE

logger = logging.getLogger(__name__)

mysql_database_name = os.environ.get("MYSQL_DATABASE")
mysql_host = os.environ.get("MYSQL_HOST")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_user = os.environ.get("MYSQL_USER")

sqlite_database_path = os.environ.get("SQLITE_DATABASE_PATH")


def connect():
    """
    Connects to the database.

    Returns:
        Database: The connected database object.

    Raises:
        DatabaseError: If failed to connect to the database.
    """
    if MYSQL_DB_NAME and MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD:
        return connect_to_mysql()

    if SQLITE_FILE:
        return connect_to_sqlite()

    raise ValueError("No database configuration found.")


@ensure_database_exists(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME)
def connect_to_mysql():
    """
    Connects to the MySQL database.

    Returns:
        MySQLDatabase: The connected MySQL database object.

    Raises:
        DatabaseError: If failed to connect to the database.
    """
    try:
        db = MySQLDatabase(
            MYSQL_DB_NAME,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
        )
        logger.info("Connected to MySQL database successfully.")
        return db
    except DatabaseError as error:
        logger.error("Failed to connect to MySQL database: %s", error)
        raise error


def connect_to_sqlite():
    """
    Connects to the SQLite database.

    Returns:
        SqliteDatabase: The connected SQLite database object.

    Raises:
        DatabaseError: If failed to connect to the database.
    """
    try:
        db = SqliteDatabase(
            SQLITE_FILE,
            pragmas={
                "journal_mode": "wal",
                "cache_size": -1 * 64000,  # 64MB
                "foreign_keys": 1,
                "ignore_check_constraints": 0,
                "synchronous": 0,
            },
        )
        logger.info("Connected to SQLite database successfully.")
        return db
    except DatabaseError as error:
        logger.error("Failed to connect to SQLite database: %s", error)
        raise error
