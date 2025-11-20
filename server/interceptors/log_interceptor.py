import logging
from grpc.aio import ServerInterceptor

endpoint_logger = logging.getLogger("endpoint_logger")
endpoint_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/endpoints.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
endpoint_logger.addHandler(file_handler)

class LogInterceptor(ServerInterceptor):
	async def intercept_service(self, continuation, handler_call_details):
		method = handler_call_details.method
		metadata = handler_call_details.invocation_metadata
		meta_str = ", ".join([f"{m.key}={m.value}" for m in metadata]) if metadata else "No metadata"
		endpoint_logger.info(f"Endpoint called: {method} | Metadata: {meta_str}")
		return await continuation(handler_call_details)