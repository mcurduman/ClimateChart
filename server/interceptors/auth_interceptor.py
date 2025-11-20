import hmac
import grpc.aio
from core.config import get_settings

settings = get_settings()

def _get_md(md, key):
    for k, v in (md or []):
        if k.lower() == key:
            return v
    return None

def _valid_api_key(value):
    return value and hmac.compare_digest(value, settings.EXPECTED_API_KEY)

class AuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
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

    def _deny(self, msg):
        async def deny(_, ctx):
            await ctx.abort(grpc.StatusCode.UNAUTHENTICATED, msg)
        return grpc.aio.unary_unary_rpc_method_handler(deny)