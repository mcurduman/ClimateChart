from proto.generated import weather_pb2, weather_pb2_grpc
import grpc 
class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def GetWeather(self, request, context):
        try:
            rec = weather_pb2.Record(
                date="2025-11-18", temperature_2m_max_c=11.2,
                temperature_2m_min_c=4.8, precipitation_sum_mm=0.4,
                pressure_msl_mean_hpa=1017.0, wind_speed_10m_max_kmh=20.5,
                relative_humidity_2m_max_pct=78
            )
            return weather_pb2.Response(city=request.city, timezone="Europe/Bucharest", records=[rec])
        except Exception as e:
            context.set_details(f'Error fetching weather data: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            print(f'Error in GetWeather: {str(e)}')
            return weather_pb2.Response()  
