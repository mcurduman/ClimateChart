import pytest
import httpx
from unittest.mock import patch, AsyncMock
from factory import Factory, Faker

BASE_URL = "http://localhost:8089/v1/weather"

class WeatherRecordFactory(Factory):
    class Meta:
        model = dict
    date = Faker("date_this_century")
    temperature_2m_max_c = Faker("pyfloat", left_digits=2, right_digits=1, positive=True)
    temperature_2m_min_c = Faker("pyfloat", left_digits=2, right_digits=1, positive=True)
    precipitation_sum_mm = Faker("pyfloat", left_digits=1, right_digits=2, positive=True)
    pressure_msl_mean_hpa = Faker("pyfloat", left_digits=4, right_digits=1, positive=True)
    wind_speed_10m_max_kmh = Faker("pyfloat", left_digits=2, right_digits=1, positive=True)
    relative_humidity_2m_max_pct = Faker("pyint", min_value=0, max_value=100)

@pytest.mark.asyncio
async def test_get_weather_missing_city():
    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL)
        print("Missing city status:", resp.status_code)
        print("Missing city body:", resp.text)
        assert resp.status_code in [400, 422]
        assert "city" in resp.text.lower()

@pytest.mark.asyncio
async def test_get_weather_valid_city():
    city = "London"
    mock_records = WeatherRecordFactory.build_batch(3)
    with patch("server.services.weather_service.WeatherService.get_forecast_by_city", new=AsyncMock(return_value=mock_records)):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/{city}")
            print("Valid city status:", resp.status_code)
            print("Valid city body:", resp.text)
            assert resp.status_code == 200
            data = resp.json()
            assert data["city"].lower() == city.lower()
            assert "records" in data
            assert isinstance(data["records"], list)
            assert all("date" in r for r in data["records"])

@pytest.mark.asyncio
async def test_get_weather_city_not_found():
    city = "NoSuchCityXYZ"
    with patch("server.services.weather_service.WeatherService.get_forecast_by_city", side_effect=LookupError("not found")):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/{city}")
            print("Not found status:", resp.status_code)
            print("Not found body:", resp.text)
            assert resp.status_code == 404
            assert "not found" in resp.text.lower()

@pytest.mark.asyncio
async def test_get_weather_external_api_error():
    city = "London"
    with patch("server.services.weather_service.WeatherService.get_forecast_by_city", side_effect=ConnectionError("external api error")):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/{city}")
            print("External API error status:", resp.status_code)
            print("External API error body:", resp.text)
            assert resp.status_code == 503 or resp.status_code == 500
            assert "error" in resp.text.lower()
