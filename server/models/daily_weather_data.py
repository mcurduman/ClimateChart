from pydantic import BaseModel
from typing import List

class DailyWeatherData(BaseModel):
    times: List[str]
    daily_temperature_2m_max: List[float]
    daily_temperature_2m_min: List[float]
    daily_precipitation_sum: List[float]
    daily_pressure_msl_mean: List[float]
    daily_wind_speed_10m_max: List[float]
    daily_relative_humidity_2m_max: List[int]
