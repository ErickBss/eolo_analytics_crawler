from models.weather import Weather
from models.db.dateTime import DateTime
from datetime import date
from config.database import db


def get_unique_hours(result: list[Weather]):
    hours = []
    for weather in result:
        if weather.hour not in hours:
            hours.append(weather.hour)
    return hours


def process_date_time_creation(result: list[Weather]):
    today = date.today()
    hours = get_unique_hours(result)

    db_models = [instance_date_time(hour, today) for hour in hours]
    db.add_all(db_models)
    db.commit()


def instance_date_time(hour: int, date: date):
    date_time = DateTime(target_date=date, target_time=hour)
    return date_time


def find_today_times():
    today = date.today()
    query_date_time = db.query(DateTime).filter_by(target_date=today).all()
    return query_date_time


def find_unique_date_time(hour: int):
    today = date.today()
    query_date_time = (
        db.query(DateTime).filter_by(target_date=today, target_time=hour).first()
    )

    return query_date_time
