from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String

Base = declarative_base()


class DataAggregate(Base):
    __tablename__ = "data_aggregate"

    geo_id = Column(Integer, primary_key=True, autoincrement=True)
    date_time_id = Column(Integer)
    mid_temp = Column(Float)
    mid_wind_speed = Column(Float)
    mid_wind_direction = Column(String(255))
    mid_real_feal = Column(Float)
    mid_humidity = Column(Float)
    mid_precipitation = Column(Float)
