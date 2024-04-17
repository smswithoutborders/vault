"""Configuration Module"""

import os

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

SQLITE_FILE = os.getenv("SQLITE_FILE")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
CUSTOM_VERIFICATION_API_KEY = os.getenv("CUSTOM_VERIFICATION_API_KEY")
CUSTOM_VERIFICATION_API_URL = os.getenv("CUSTOM_VERIFICATION_API_URL")


def validate_config():
    """
    Validate the database configuration.

    Raises:
        ValueError: If neither MySQL nor SQLite configuration is provided.
    """
    if (
        not (MYSQL_HOST and MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE)
        and not SQLITE_FILE
    ):
        raise ValueError("At least one database configuration must be provided")


validate_config()
