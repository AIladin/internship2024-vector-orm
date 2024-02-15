from sqlalchemy import create_engine, orm
from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings

engine = create_engine(settings.sync_connection_str)
asnyc_engine = create_async_engine(
    settings.async_connection_str
)
sessionmaker = orm.sessionmaker(bind=engine)
