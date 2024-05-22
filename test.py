import asyncio

import databases
import ormar
import sqlalchemy
from db import GRCEventCreator, GRCEvent
from init_db import ormar_base_config


ormar_base_config.metadata.create_all(ormar_base_config.engine)
db = ormar_base_config.database


async def test():
    if not db.is_connected:
        await db.connect()
    await GRCEventCreator.objects.delete(id=1)
    await GRCEventCreator.objects.create(id=1)
    for i in await GRCEvent.objects.all():
        await GRCEvent.objects.delete(id=i.id)

    if db.is_connected:
        await db.disconnect()

asyncio.run(test())