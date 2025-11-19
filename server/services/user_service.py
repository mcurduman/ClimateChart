import time, os
from generated import user_pb2, user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def StartEmailVerification(self, request, context):
        return user_pb2.StartEmailVerificationResponse(
            user_id=f"u_{int(time.time())}",
            message=f"Verification sent to {request.email}"
        )

    def ConfirmEmail(self, request, context):
        return user_pb2.ConfirmEmailResponse(success=True)

    def Login(self, request, context):
        # JWT removed: return only user_id and username
        return user_pb2.LoginResponse(
            user_id="u_123",
            username=request.username
        )

    def CreateApiKey(self, request, context):
        return user_pb2.CreateApiKeyResponse(api_key="api_key_demo", key_id="key_123", expires_at="2025-12-31T23:59:59Z")

    def ListApiKeys(self, request, context):
        key = user_pb2.ApiKeyInfo(
            key_id="key_123", label="default", scope="*", status=user_pb2.ACTIVE,
            created_at="2025-01-01T00:00:00Z", expires_at="2025-12-31T23:59:59Z", last_used_at="2025-11-18T00:00:00Z"
        )
        return user_pb2.ListApiKeysResponse(keys=[key])

    def GetMe(self, request, context):
        return user_pb2.GetMeResponse(
            user_id="u_123",
            username="demo",
            email="demo@example.com",
            email_verified=True,
            created_at="2025-01-01T00:00:00Z"
        )
