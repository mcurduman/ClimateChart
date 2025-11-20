import logging
import hmac
import grpc.aio
from core.config import get_settings

settings = get_settings()


def _get_md(md, key):
    try:
        for k, v in (md or []):
            if k.lower() == key:
                return v
        return None
    except Exception as e:
        logging.error(f"Error in _get_md: {e}")
        return None


def _valid_api_key(value):
    try:
        return value and hmac.compare_digest(value, settings.EXPECTED_API_KEY)
    except Exception as e:
        logging.error(f"Error in _valid_api_key: {e}")
        return False

class AuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        try:
            method = handler_call_details.method
            md = handler_call_details.invocation_metadata
            api_key = _get_md(md, settings.API_KEY_HEADER)

            if method in settings.PUBLIC_METHODS:
                return await continuation(handler_call_details)
            if method in settings.API_KEY_METHODS:
                if not _valid_api_key(api_key):
                    return self._deny("API key required")
                return await continuation(handler_call_details)
            return await continuation(handler_call_details)
        except Exception as e:
            logging.error(f"AuthInterceptor error: {e}")
            return self._deny("Authentication error")

    def _deny(self, msg):
        async def deny(_, ctx):
            try:
                logging.warning(f"Denied authentication: {msg}")
                await ctx.abort(grpc.StatusCode.UNAUTHENTICATED, msg)
            except Exception as e:
                logging.error(f"Error during deny abort: {e}", exc_info=True)
        return grpc.aio.unary_unary_rpc_method_handler(deny)