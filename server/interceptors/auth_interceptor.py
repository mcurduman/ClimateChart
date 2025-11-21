import logging
import hmac
import grpc
from core.config import get_settings
from services.api_key_service import ApiKeyService

settings = get_settings()
api_key_service = ApiKeyService()


def _get_md(md, key):
    try:
        key = key.lower()
        for k, v in (md or []):
            if k.lower() == key:
                return v
        return None
    except Exception as e:
        logging.error(f"Error in _get_md: {e}")
        return None


async def _valid_api_key(value, user_email):
    try:
        if not value or not user_email:
            return False
        key_info = await api_key_service.get_key(user_email)
        if not key_info or not key_info.value:
            return False
        return hmac.compare_digest(value, key_info.value)
    except Exception as e:
        logging.error(f"Error in _valid_api_key: {e}")
        return False

class AuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        try:
            logging.info(f"AuthInterceptor: intercepting service {handler_call_details.method}")
            method = handler_call_details.method
            md = handler_call_details.invocation_metadata
            api_key = _get_md(md, settings.API_KEY_HEADER)
            user_email =  _get_md(md, "x-user-email")

            if method in settings.PUBLIC_METHODS:
                return await continuation(handler_call_details)
            if method in settings.API_KEY_METHODS:
                key_info = None
                if user_email:
                    key_info = await api_key_service.get_key(user_email)
                expected_key = key_info.value if key_info and key_info.value else None
                if not await _valid_api_key(api_key, user_email):
                    logging.warning(f"API key mismatch: expected='{expected_key}' received='{api_key}' for user_email='{user_email}'")
                    return self._deny("API key required or invalid")
                return await continuation(handler_call_details)
            return await continuation(handler_call_details)
        except Exception as e:
            logging.error(f"AuthInterceptor error: {e}")
            return self._deny("Authentication error")

    def _deny(self, msg):
        def deny(_, ctx):
            try:
                logging.warning(f"Denied authentication: {msg}")
                ctx.abort(grpc.StatusCode.UNAUTHENTICATED, msg)
            except Exception as e:
                logging.error(f"Error during deny abort: {e}", exc_info=True)
        return grpc.unary_unary_rpc_method_handler(deny)