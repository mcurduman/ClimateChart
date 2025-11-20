import asyncio
import grpc.aio
from interceptors.auth_interceptor import AuthInterceptor
from interceptors.log_interceptor import LogInterceptor
from handlers.weather_service_servicer import WeatherServiceServicer
from proto.generated import weather_pb2_grpc
import logging 

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting server...")

async def serve():
    logger.info("Trying to start gRPC aio server...")
    try:
        server = grpc.aio.server(
            interceptors=[AuthInterceptor(), LogInterceptor()]
        )
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
        server.add_insecure_port("[::]:9092")
        logger.info("[gRPC] aio server running on port 9092...")
        await server.start()
        await server.wait_for_termination()
    except Exception as e:
        logger.exception(f"Exception during aio server startup: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(serve())
