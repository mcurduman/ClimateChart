import grpc
import logging
import base64
import os
from proto.generated import user_pb2, user_pb2_grpc
from services.user_service import UserService
from services.api_key_service import ApiKeyService
from services.email_service import EmailService
import random

logger = logging.getLogger(__name__)

INTERNAL_SERVER_ERROR_MSG = "Internal server error."

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = UserService()
        self.api_keys = ApiKeyService()
        self.emails = EmailService()

    async def SignUp(self, request, context):
        name = (request.name or "").strip()
        email = (request.email or "").strip().lower()
        password = (request.password or "").strip()
        if not name or not email or not password:
            logger.warning(f"SignUp missing fields: name={name}, email={email}")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Name, email, and password are required.")
        try:
            user_id = base64.b64encode(os.urandom(8)).decode()
            result = await self.users.sign_up(user_id, name, email, password)
            if not result:
                logger.warning(f"SignUp failed for email: {email}")
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, "User already exists or error occurred.")
            logger.info(f"User signed up: {email}")
            return user_pb2.SignUpResponse(user_id=user_id)
        except Exception as e:
            logger.error(f"SignUp error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def Login(self, request, context):
        email = (request.email or "").strip().lower()
        password = (request.password or "").strip()
        if not email or not password:
            logger.warning(f"Login missing fields: email={email}")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Email and password are required.")
        try:
            user = await self.users.login(email, password)
            if not user:
                logger.warning(f"Login failed for email: {email}")
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid credentials.")
            logger.info(f"User logged in: {user.email}")
            return user_pb2.LoginResponse(
                user_id=user.user_id,
                name=user.name,
                email=user.email,
            )
        except ConnectionError as e:
            logger.error(f"Login connection error: {e}")
            await context.abort(grpc.StatusCode.UNAVAILABLE, str(e))
        except LookupError as e:
            logger.error(f"Login lookup error: {e}")
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            logger.error(f"Login error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def ConfirmEmail(self, request, context):
        email = (request.email or "").strip()
        if not email:
            logger.warning("ConfirmEmail missing email")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "email is required.")
        try:
            verification_saved = await self.emails.get_verification_by_email(email)
            if not verification_saved:
                logger.warning("ConfirmEmail missing email")
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "email is required.")
            if verification_saved.get("code") != (request.code or "").strip():
                logger.warning("ConfirmEmail invalid code")
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid verification code.")
            logger.info(f"ConfirmEmail code verified for email: {email}")
            user = await self.users.find_by_email(email)
            if not user:
                logger.warning(f"ConfirmEmail user not found for email: {email}")
                await context.abort(grpc.StatusCode.NOT_FOUND, "User not found.")
            success = await self.users.verify_email(user.user_id)
            logger.info(f"ConfirmEmail called for email: {email}, success: {success}")
            return user_pb2.ConfirmEmailResponse(success=success)
        except LookupError as e:
            logger.error(f"ConfirmEmail lookup error: {e}")
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            logger.error(f"ConfirmEmail error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def GetMe(self, request, context):
        email = (request.email or "").strip().lower()
        logger.info(f"[GetMe] Incoming request: email={email}")
        if not email:
            logger.warning("[GetMe] Missing email param")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "email is required.")
        try:
            user = await self.users.find_by_email(email)
            if not user:
                logger.warning(f"[GetMe] User not found for email: {email}")
                await context.abort(grpc.StatusCode.NOT_FOUND, "User not found.")
            logger.info(f"[GetMe] User found: user_id={user.user_id}, name={user.name}, email={user.email}, email_verified={user.email_verified}")
            response = user_pb2.GetMeResponse(
                user_id=user.user_id,
                name=user.name,
                email=user.email,
                email_verified=user.email_verified
            )
            logger.info(f"[GetMe] Response: {response}")
            return response
        except ConnectionError as e:
            logger.error(f"[GetMe] Connection error: {e}")
            await context.abort(grpc.StatusCode.UNAVAILABLE, str(e))
        except LookupError as e:
            logger.error(f"[GetMe] Lookup error: {e}")
            await context.abort(grpc.StatusCode.NOT_FOUND, str(e))
        except Exception as e:
            logger.error(f"[GetMe] Internal error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def CreateApiKey(self, request, context):
        user_email = (request.user_email or "").strip().lower()
        if not user_email:
            logger.warning("CreateApiKey missing user_email")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "user_email is required.")
        try:
            info_user = await self.users.find_by_email(user_email)
            if not info_user:
                logger.warning(f"CreateApiKey user not found for email: {user_email}")
                await context.abort(grpc.StatusCode.NOT_FOUND, "User not found.")
            if info_user.email_verified is False:
                logger.warning(f"CreateApiKey email not verified for email: {user_email}")
                await context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Email not verified.")
            api_key = await self.api_keys.create_key(user_email)
            if not api_key:
                logger.warning(f"CreateApiKey failed for user_email: {user_email}")
                await context.abort(grpc.StatusCode.INTERNAL, "Failed to create API key.")
            logger.info(f"API key created for user_email: {user_email}")
            return user_pb2.ApiKeyInfo(
                user_email=api_key.user_email,
                value=api_key.value,
                created_at=api_key.created_at
            )
        except Exception as e:
            logger.error(f"CreateApiKey error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def GetApiKey(self, request, context):
        user_email = (request.user_email or "").strip().lower()
        if not user_email:
            logger.warning("GetApiKey missing user_email")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "user_email is required.")
        try:
            api_key = await self.api_keys.get_key(user_email)
            if not api_key:
                logger.warning(f"GetApiKey not found for user_email: {user_email}")
                await context.abort(grpc.StatusCode.NOT_FOUND, "API key not found.")
            logger.info(f"API key found for user_email: {user_email}")
            return user_pb2.ApiKeyInfo(
                user_email=api_key.user_email,
                value=api_key.value,
                created_at=api_key.created_at
            )
        except Exception as e:
            logger.error(f"GetApiKey error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)

    async def SendVerificationEmail(self, request, context):
        email = (request.email or "").strip().lower()
        if not email:
            logger.warning("SendVerificationEmail missing email")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "email is required.")
        try:
            existing_verification = await self.emails.get_verification_by_email(email)
            if existing_verification:
                logger.info(f"Code already sent for email: {email}")
                return user_pb2.SendVerificationEmailResponse(success=False, message="Verification code already sent. Please check your email.")
            code = str(random.randint(100000, 999999))
            await self.emails.create_verification(email, code)
            await self.emails.send_verification_email(email, code)
            logger.info(f"SendVerificationEmail called for email: {email}, code: {code}")
            return user_pb2.SendVerificationEmailResponse(success=True, message="Verification email sent.")
        except Exception as e:
            logger.error(f"SendVerificationEmail error: {e}")
            await context.abort(grpc.StatusCode.INTERNAL, INTERNAL_SERVER_ERROR_MSG)