from sqlalchemy.ext.asyncio import create_async_engine
from os import getenv as ENV
import sqlalchemy

bdurl = ENV("DBURL")
engine = create_async_engine(bdurl, echo=True)
