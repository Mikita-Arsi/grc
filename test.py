import asyncio

import databases
import ormar
import sqlalchemy
from sqlalchemy import Column
from db import GRCEventCreator, GRCEvent
from init_db import ormar_base_config


ormar_base_config.metadata.create_all(ormar_base_config.engine)
db = ormar_base_config.database


async def test():
    if not db.is_connected:
        await db.connect()
    ormar_base_config.metadata.create_all(ormar_base_config.engine)
    print(await GRCEvent.objects.all())

    if db.is_connected:
        await db.disconnect()

asyncio.run(test())