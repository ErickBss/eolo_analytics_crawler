import asyncio
from models.weather import Weather
from services.crawlers.weather import crawler as weatherCrawler
from services.crawlers.accuWeather import crawler as accuWeatherCrawler
from services.date_time.index import (
    process_date_time_creation,
    find_unique_date_time,
)
from services.aggregate.index import agg_data
import schedule
from time import sleep

from config.database import db


def store_crawler_date(result: list[Weather]):
    db_models = []

    for weather in result:
        print("hour", weather.hour)
        date_time = find_unique_date_time(weather.hour)
        print("date_time", date_time)
        weather_db_instance = weather.db_instance(
            1, date_time_id=date_time.date_time_id
        )

        db_models.append(weather_db_instance)

    db.add_all(db_models)


def main():
    print("Running crawlers")
    result = []

    # executa processos de crawler nas fontes disponíveis
    asyncio.run(weatherCrawler(result))
    asyncio.run(accuWeatherCrawler(result))

    # cria registro de horários de previsão do tempo
    process_date_time_creation(result)

    # instacia de modelos do banco
    print("storing result")
    store_crawler_date(result)
    print("result stored")

    # estima e análise fontes de dados configuradas
    print("aggregating data")
    agg_data(result)

    # salva no banco de dados
    print("storing data")
    db.commit()


# cron job
schedule.every().hour.do(main())


while True:
    schedule.run_pending()
    print("Sleeping...")
    sleep(3600)  # 1h

# if __name__ == "__main__":
#     main()
