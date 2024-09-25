from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Date

Base = declarative_base()


class DateTime(Base):
    __tablename__ = "date_time"

    date_time_id = Column(Integer, primary_key=True, autoincrement=True)
    target_date = Column(Date)
    target_time = Column(Integer)
