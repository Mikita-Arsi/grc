import ormar

from datetime import datetime
from init_db import ormar_base_config


class GRCUser(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    tg_id: int = ormar.BigInteger(unique=True, nullable=False)
    username: str = ormar.String(max_length=200, nullable=True)
    first_name: str = ormar.String(max_length=200)
    last_name: str = ormar.String(max_length=200, nullable=True)
    location: str = ormar.String(max_length=200, nullable=True)
    description: str = ormar.String(max_length=4096, nullable=True)
    join_date: datetime = ormar.DateTime(nullable=False)


class GRCEvent(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    datetime: datetime = ormar.DateTime(nullable=False)
    location: str = ormar.String(max_length=300, nullable=False)
    location_url: str = ormar.String(max_length=300, nullable=False)
    title: str = ormar.String(max_length=300, nullable=False)
    description: str = ormar.String(max_length=2000, nullable=False)
    themes: str = ormar.String(max_length=4096, nullable=False)


class GRCEventCreator(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    datetime: datetime = ormar.DateTime(nullable=True)
    location: str = ormar.String(max_length=300, nullable=True)
    location_url: str = ormar.String(max_length=300, nullable=True)
    title: str = ormar.String(max_length=300, nullable=True)
    description: str = ormar.String(max_length=2000, nullable=True)
    themes: str = ormar.String(max_length=4096, nullable=True)


class GRCVisitor(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    tg_id: int = ormar.BigInteger(nullable=False)
    event_id: int = ormar.Integer(nullable=False)
    is_online: int = ormar.Boolean(nullable=False)


class GRCProtocol(ormar.Model):
    ormar_config = ormar_base_config.copy()

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    text: int = ormar.String(max_length=4096)
    event_id: int = ormar.Integer(nullable=False, unique=True)
    tg_id: int = ormar.BigInteger(nullable=False)
