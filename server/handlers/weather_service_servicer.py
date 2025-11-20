# server/grpc/weather_servicer.py
from proto.generated import weather_pb2, weather_pb2_grpc
import grpc
from services.weather_service import WeatherService

class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):

    async def GetWeather(self, request, context):
        svc = WeatherService()
        city = (request.city or "").strip()
        if not city:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "city is required")
        try:
            records = await svc.get_forecast_by_city(city)
            print("SERVICE DATA:", records)
            proto_records = [
                weather_pb2.Record(
                    date=r.get("date", ""),
                    temperature_2m_max_c=r.get("temperature_2m_max_c", 0.0),
                    temperature_2m_min_c=r.get("temperature_2m_min_c", 0.0),
                    precipitation_sum_mm=r.get("precipitation_sum_mm", 0.0),
                    pressure_msl_mean_hpa=r.get("pressure_msl_mean_hpa", 0.0),
                    wind_speed_10m_max_kmh=r.get("wind_speed_10m_max_kmh", 0.0),
                    relative_humidity_2m_max_pct=int(r.get("relative_humidity_2m_max_pct", 0)),
                )
                for r in records
            ]
            return weather_pb2.Response(
                city=city,
                timezone="",
                records=proto_records,
            )
        except ConnectionError as e:
            await context.abort(grpc.StatusCode.UNAVAILABLE, str(e))
        except LookupError as e:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, f"Error fetching weather data: {e}")
