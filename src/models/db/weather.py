from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Enum
import enum


Base = declarative_base()


class WindDirection(enum.Enum):
    NORTH = "N"
    NORTHEAST = "NE"
    EAST = "E"
    SOUTHEAST = "SE"
    SOUTH = "S"
    SOUTHWEST = "SW"
    WEST = "W"
    NORTHWEST = "NW"


class Model(Base):
    __tablename__ = "weather_crawler"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    date_time_id = Column(Integer)
    geo_id = Column(Integer)
    est_humidity = Column(Integer, nullable=True)
    est_real_feal = Column(Integer)
    est_temperature = Column(Integer)
    est_wind_speed = Column(Integer)
    est_wind_direction = Column(Enum(WindDirection))
