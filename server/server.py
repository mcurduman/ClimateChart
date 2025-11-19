import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))
import grpc
from concurrent import futures
from auth_interceptor import AuthInterceptor
from services.user_service import UserService
from services.weather_service import WeatherService
from generated import user_pb2_grpc, weather_pb2_grpc

print("Starting server...", flush=True)

def serve():
    print("Trying to start gRPC server...", flush=True)
    try:
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            interceptors=[AuthInterceptor()],
        )
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
        server.add_insecure_port("[::]:50051")
        print("[gRPC] Server running on port 50051...", flush=True)
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print("Exception during server startup:", repr(e), flush=True)

if __name__ == "__main__":
    serve()
