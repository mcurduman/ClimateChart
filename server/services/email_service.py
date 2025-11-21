import logging
from repositories.email_repository import EmailRepository
import mailtrap as mt 
from core.config import get_settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.repo = EmailRepository()

    async def init(self):
        await self.repo.ensure_ttl_index()

    async def create_verification(self, user_email: str, code: str):
        return await self.repo.insert_verification(user_email, code)

    async def get_verification_by_email(self, user_email: str):
        return await self.repo.get_by_user_email(user_email)
    
    async def send_verification_email(self, user_email: str, code: str):
        settings = get_settings()
        mail = mt.MailFromTemplate(
            sender=mt.Address(email=settings.DEFAULT_SENDER, name="ClimateChart Service"),
            to=[mt.Address(email=user_email)],
            template_uuid=settings.TEMPLATE_UUID,
            template_variables={
            "user_email": user_email,
            "verification-code": code
            }
        )
        client = mt.MailtrapClient(token=settings.PASSWORD)
        response = client.send(mail)
        print(response)
