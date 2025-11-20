import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from httpx import AsyncClient
from httpx import HTTPError, TimeoutException
import logging 
from repositories.weather_repository import WeatherRepository
from core.config import get_settings
from models.daily_weather_data import DailyWeatherData

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.client = openmeteo_requests.Client(session=retry_session)
        self.url = get_settings().API_URL
        self.repo = WeatherRepository()

    async def save_records(self, records, city, fetch_date):
        doc = {
            "city": city,
            "fetch_date": fetch_date,
            "records": records
        }
        try:
            return await self.repo.insert(doc)
        except Exception as e:
            logger.error(f"[WeatherService] Error caching records: {e}")
            raise

    def _build_daily_records(self, daily_data: DailyWeatherData):
        records = []
        for i in range(len(daily_data.times)):
            record = {
                "date": daily_data.times[i],
                "temperature_2m_max_c": float(daily_data.daily_temperature_2m_max[i]) if i < len(daily_data.daily_temperature_2m_max) else None,
                "temperature_2m_min_c": float(daily_data.daily_temperature_2m_min[i]) if i < len(daily_data.daily_temperature_2m_min) else None,
                "precipitation_sum_mm": float(daily_data.daily_precipitation_sum[i]) if i < len(daily_data.daily_precipitation_sum) else None,
                "pressure_msl_mean_hpa": float(daily_data.daily_pressure_msl_mean[i]) if i < len(daily_data.daily_pressure_msl_mean) else None,
                "wind_speed_10m_max_kmh": float(daily_data.daily_wind_speed_10m_max[i]) if i < len(daily_data.daily_wind_speed_10m_max) else None,
                "relative_humidity_2m_max_pct": int(daily_data.daily_relative_humidity_2m_max[i]) if i < len(daily_data.daily_relative_humidity_2m_max) else None,
            }
            records.append(record)
        return records

    def parse_daily_response(self, response) -> list:
        if not hasattr(response, "Daily"):
            logger.warning("Response has no 'Daily' attribute.")
            return []

        try:
            daily_obj = response.Daily()
            daily_vars = [daily_obj.Variables(i).ValuesAsNumpy() for i in range(6)]
            daily_temperature_2m_max, daily_temperature_2m_min, daily_precipitation_sum, \
            daily_pressure_msl_mean, daily_wind_speed_10m_max, daily_relative_humidity_2m_max = daily_vars

            dates = pd.date_range(
                start=pd.to_datetime(daily_obj.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily_obj.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily_obj.Interval()),
                inclusive="left"
            )
            times = [d.strftime("%Y-%m-%d") for d in dates]

            daily_data = DailyWeatherData(
                times=times,
                daily_temperature_2m_max=daily_temperature_2m_max.tolist(),
                daily_temperature_2m_min=daily_temperature_2m_min.tolist(),
                daily_precipitation_sum=daily_precipitation_sum.tolist(),
                daily_pressure_msl_mean=daily_pressure_msl_mean.tolist(),
                daily_wind_speed_10m_max=daily_wind_speed_10m_max.tolist(),
                daily_relative_humidity_2m_max=daily_relative_humidity_2m_max.tolist(),
            )
            
            records = self._build_daily_records(daily_data)
            return records

        except (AttributeError, IndexError, ValueError, TypeError) as e:
            logger.error(f"Invalid or incomplete daily data structure: {e}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error parsing daily response: {e}")
            return []

    async def get_geocoding(self, name: str, count: int = 1, format: str = "json", language: str = "en"):
        base_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": name,
            "count": count,
            "format": format,
            "language": language,
        }
        try:
            async with AsyncClient() as async_client:
                response = await async_client.get(base_url, params=params)
                response.raise_for_status()
                try:
                    data = response.json()
                except Exception as json_err:
                    raise ValueError(f"Invalid JSON response: {json_err}")
                if not data.get("results"):
                    raise LookupError(f"No geocoding results for '{name}'")
                try:
                    lat = float(data["results"][0]["latitude"])
                    lon = float(data["results"][0]["longitude"])
                except (KeyError, IndexError, ValueError) as parse_err:
                    raise ValueError(f"Malformed geocoding data: {parse_err}")
                return lat, lon
        except ValueError as e:
            logger.error(f"Geocoding error: {e}")
            raise
        except Exception as e:
            logger.error(f"Geocoding request failed: {e}")
            raise

    async def get_forecast(self, latitude: float, longitude: float) -> list:
        try:
            openmeteo = openmeteo_requests.AsyncClient()
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "pressure_msl_mean",
                    "wind_speed_10m_max",
                    "relative_humidity_2m_max"
                ],
                "wind_speed_unit": "kmh",
                "timezone": "auto",
                "past_days": 7,
                "forecast_days": 7
            }

            responses = await openmeteo.weather_api(url, params=params)
            if not responses:
                raise LookupError("Empty response from Open-Meteo API")

            response = responses[0]
            return self.parse_daily_response(response)
        except (HTTPError, TimeoutException) as net_err:
            logger.error(f"[WeatherService] Network error: {net_err}")
            raise ConnectionError(f"Failed to reach Open-Meteo API: {net_err}") from net_err
        except LookupError as not_found_err:
            logger.error(f"[WeatherService] No data found: {not_found_err}")
            raise
        except ValueError as parse_err:
            logger.error(f"[WeatherService] Data parsing error: {parse_err}")
            raise
        except Exception as e:
            logger.error(f"[WeatherService] Unexpected error: {e}")
            raise RuntimeError(f"Unexpected error while fetching forecast: {e}") from e
        
    async def get_forecast_by_city(self, city: str) -> list:
        from datetime import date
        today = date.today().isoformat()
        try:
            latitude, longitude = await self.get_geocoding(city)
            records = await self.get_forecast(latitude, longitude)
            await self.save_records(records, city, today)
            return records
        except Exception as e:
            logger.error(f"[WeatherService] Error getting daily forecast for city '{city}': {e}")
            raise