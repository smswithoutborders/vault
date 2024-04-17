"""Database Models."""

from datetime import datetime
from peewee import Model, CharField, DateTimeField

from db import connect
from utils import create_tables

database = connect()


class Entities(Model):
    """Model representing Entities."""

    eid = CharField(primary_key=True)
    msisdn_hash = CharField()
    username = CharField()
    password_hash = CharField()
    created_at = DateTimeField(default=datetime.now)

    # pylint: disable=R0903
    class Meta:
        """Meta class to define database connection."""

        database = database
        table_name = "entities"


create_tables([Entities], database)
