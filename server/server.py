import grpc
from concurrent import futures
from interceptors.auth_interceptor import AuthInterceptor
from services.weather_service import WeatherService
from proto.generated import weather_pb2_grpc

print("Starting server...", flush=True)

def serve():
    print("Trying to start gRPC server...", flush=True)
    try:
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            interceptors=[AuthInterceptor()],
        )
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(), server)
        server.add_insecure_port("[::]:9092")
        print("[gRPC] Server running on port 9092...", flush=True)
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print("Exception during server startup:", repr(e), flush=True)

if __name__ == "__main__":
    serve()
