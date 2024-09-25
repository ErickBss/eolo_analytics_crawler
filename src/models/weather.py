import re
from models.db.weather import Model


# formata dados
class Weather:
    def __init__(self) -> None:
        self.hour = None
        self.humidity = 0
        self.real_feal = None
        self.temperature = None
        self.wind_direction = None
        self.wind_speed = None
        self.source_id = None

    # transforma string em número
    def transform_to_number(self, value: str):
        return int(re.sub("[^0-9]", "", value))

    # armazena/formata dados
    def set_hour(self, hour: str):
        if type(hour) is not str:
            raise Exception("Hour is not a string")

        if "PM" in hour:
            self.hour = self.transform_to_number(hour) + 12
        elif ":" in hour:
            value = hour.split(":")
            self.hour = self.transform_to_number(value[0])
        else:
            self.hour = self.transform_to_number(hour)

    def set_humidity(self, humidity=""):
        if humidity:
            self.humidity = self.transform_to_number(humidity)

    def set_attr(self, key, value):
        if not value:
            raise Exception(f"{key} is null")

        if key == "wind_direction":
            self.wind_direction = value
        elif key == "source_id":
            self.source_id = value
        else:
            parsed_value = self.transform_to_number(value)
            setattr(self, key, parsed_value)

    # cria modelo do banco de dados
    def db_instance(
        self,
        geo_id: int,
        date_time_id: int,
    ):
        print(self.__dict__)
        return Model(
            source_id=self.source_id,
            geo_id=geo_id,
            date_time_id=date_time_id,
            est_humidity=self.humidity,
            est_real_feal=self.real_feal,
            est_temperature=self.temperature,
            est_wind_speed=self.wind_speed,
            est_wind_direction=self.wind_direction,
        )
