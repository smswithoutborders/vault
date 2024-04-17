"""Module for connecting to a database."""

import logging
from peewee import MySQLDatabase, SqliteDatabase, DatabaseError
from utils import ensure_database_exists

from config import MYSQL_HOST, MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_USER, SQLITE_FILE

logger = logging.getLogger(__name__)


def connect():
    """
    Connects to the database.

    Returns:
        Database: The connected database object.

    Raises:
        DatabaseError: If failed to connect to the database.
    """
    if MYSQL_DATABASE and MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD:
        return connect_to_mysql()

    if SQLITE_FILE:
        return connect_to_sqlite()

    raise ValueError("No database configuration found.")


@ensure_database_exists(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
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
            MYSQL_DATABASE,
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
