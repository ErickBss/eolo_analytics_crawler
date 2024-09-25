from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Source(Base):
    __tablename__ = "data_source"

    source_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    web_address = Column(String(250))
