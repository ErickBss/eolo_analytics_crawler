from models.weather import Weather
from services.date_time.index import find_today_times
from models.db.dataAggregate import DataAggregate
from config.database import db


def average(value: list[int]):
    return sum(value) / len(value)


def agg_data(result: list[Weather]):
    values = {
        "temperature": [],
        "wind_speed": [],
        "wind_direction": [],
        "real_feal": [],
        "humidity": [],
    }

    # busca horários criados no dia de hoje
    date_times = find_today_times()

    for date_time in date_times:
        # filtra resultados de fontes por horário
        filtered_results = filter(
            lambda item: item.hour == date_time.target_time, result
        )

        for weather in filtered_results:
            weather_dict = weather.__dict__

            for key, value in weather_dict.items():
                if key in values.keys():
                    values[key].append(value)

        # consolida dados das fontes
        data_agg = DataAggregate(
            geo_id=1,
            date_time_id=date_time.date_time_id,
            mid_temp=average(values["temperature"]),
            mid_wind_direction=values["wind_direction"][0],
            mid_wind_speed=average(values["wind_speed"]),
            mid_real_feal=average(values["real_feal"]),
            mid_humidity=average(values["humidity"]),
            mid_precipitation=0,
        )

        db.add(data_agg)
