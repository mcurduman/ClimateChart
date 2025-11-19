import hmac
import grpc
from core.config import get_settings

settings = get_settings()

def _get_md(md, key):
    for k, v in (md or []):
        if k.lower() == key:
            return v
    return None

def _valid_api_key(value):
    return value and hmac.compare_digest(value, settings.EXPECTED_API_KEY)

class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, details):
        method = details.method
        md = details.invocation_metadata
        api_key = _get_md(md, settings.API_KEY_HEADER)

        if method in settings.PUBLIC_METHODS:
            return continuation(details)
        if method in settings.API_KEY_METHODS:
            if not _valid_api_key(api_key):
                return self._deny("API key required")
            return continuation(details)
        return continuation(details)

    def _deny(self, msg):
        def deny(_, ctx):
            ctx.abort(grpc.StatusCode.UNAUTHENTICATED, msg)
        return grpc.unary_unary_rpc_method_handler(deny)