import asyncio
import grpc.aio
from interceptors.auth_interceptor import AuthInterceptor
from interceptors.log_interceptor import LogInterceptor
from handlers.weather_service_servicer import WeatherServiceServicer
from handlers.user_service_servicer import UserServiceServicer
from proto.generated import weather_pb2_grpc
from proto.generated import user_pb2_grpc
from services.email_service import EmailService
from services.api_key_service import ApiKeyService
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
        
        email_service = EmailService()
        await email_service.init()
        api_key_service = ApiKeyService()
        await api_key_service.init()

        server = grpc.aio.server(
            interceptors=[AuthInterceptor(), LogInterceptor()]
        )
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
        user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
        server.add_insecure_port("[::]:9092")
        logger.info("[gRPC] aio server running on port 9092...")
        await server.start()
        await server.wait_for_termination()
    except Exception as e:
        logger.exception(f"Exception during aio server startup: {repr(e)}")

if __name__ == "__main__":
    asyncio.run(serve())
