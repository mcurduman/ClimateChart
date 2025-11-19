import os, hmac, grpc

API_KEY_HEADER = "x-api-key"
AUTHZ_HEADER = "authorization"
EXPECTED_API_KEY = os.getenv("X_API_KEY", "supersecret")

PUBLIC_METHODS = {
    "/user.UserService/StartEmailVerification",
    "/user.UserService/ConfirmEmail",
    "/user.UserService/Login",
    "/user.UserService/GetMe",
    "/user.UserService/CreateApiKey",
    "/user.UserService/ListApiKeys",
    "/user.UserService/Logout",
    "/weather.WeatherService/GetDaily",
}

def _get_md(md, key):
    for k, v in (md or []):
        if k.lower() == key:
            return v
    return None

def _valid_api_key(value): return value and hmac.compare_digest(value, EXPECTED_API_KEY)

class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, details):
        method = details.method
        md = details.invocation_metadata
        api_key = _get_md(md, API_KEY_HEADER)

        if method in PUBLIC_METHODS:
            return continuation(details)
        if method in API_KEY_METHODS:
            if not _valid_api_key(api_key):
                return self._deny("API key required")
            return continuation(details)
        return continuation(details)

    def _deny(self, msg):
        def deny(_, ctx):
            ctx.abort(grpc.StatusCode.UNAUTHENTICATED, msg)
        return grpc.unary_unary_rpc_method_handler(deny)
