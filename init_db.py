import databases
import ormar
import sqlalchemy

from config import DB

ormar_base_config = ormar.OrmarConfig(
    database=databases.Database(DB),
    metadata=sqlalchemy.MetaData(),
    engine=sqlalchemy.create_engine(DB),
)

