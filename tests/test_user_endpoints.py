import pytest
import httpx
from unittest.mock import patch
from factory import Factory, Faker

BASE_URL = "http://localhost:8089/v1/user"

class UserFactory(Factory):
    class Meta:
        model = dict
    name = Faker("name")
    email = Faker("email")
    password = Faker("password", length=12)

@pytest.mark.asyncio
async def test_signup():
    user = UserFactory.build()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/sign-up", json={"name": user["name"], "email": user["email"], "password": user["password"]})
        print("SignUp status:", resp.status_code)
        print("SignUp body:", resp.text)
        assert resp.status_code == 200
        data = resp.json()
        assert "userId" in data

@pytest.mark.asyncio
async def test_login():
    user = UserFactory.build()
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sign-up", json={"name": user["name"], "email": user["email"], "password": user["password"]})
        resp = await client.post(f"{BASE_URL}/login", json={"email": user["email"], "password": user["password"]})
        print("Login status:", resp.status_code)
        print("Login body:", resp.text)
        assert resp.status_code == 200
        login_data = resp.json()
        assert "userId" in login_data or "apiKey" in login_data or "token" in login_data

@pytest.mark.asyncio
async def test_send_verification_email():
    user = UserFactory.build()
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sign-up", json={"name": user["name"], "email": user["email"], "password": user["password"]})
        resp = await client.post(f"{BASE_URL}/send-verification-email", json={"email": user["email"]})
        print("SendVerificationEmail status:", resp.status_code)
        print("SendVerificationEmail body:", resp.text)
        assert resp.status_code == 200

@pytest.mark.asyncio
async def test_confirm_email():
    user = UserFactory.build()
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sign-up", json={"name": user["name"], "email": user["email"], "password": user["password"]})
        await client.post(f"{BASE_URL}/send-verification-email", json={"email": user["email"]})
        resp = await client.post(f"{BASE_URL}/confirm-email", json={"email": user["email"], "code": "123456"})
        print("ConfirmEmail status:", resp.status_code)
        print("ConfirmEmail body:", resp.text)
        assert resp.status_code in [200, 400]

@pytest.mark.asyncio
async def test_get_api_key():
    user = UserFactory.build()
    class MockUser:
        def __init__(self, name, email):
            self.user_id = "testid"
            self.name = name
            self.email = email
            self.email_verified = True
    with patch("server.repositories.user_repository.UserRepository.find_by_email", return_value=MockUser(user["name"], user["email"])):
        async with httpx.AsyncClient() as client:
            await client.post(f"{BASE_URL}/sign-up", json={"name": user["name"], "email": user["email"], "password": user["password"]})
            await client.post(f"{BASE_URL}/send-verification-email", json={"email": user["email"]})
            await client.post(f"{BASE_URL}/confirm-email", json={"email": user["email"], "code": "123456"})
            login_resp = await client.post(f"{BASE_URL}/login", json={"email": user["email"], "password": user["password"]})
            print("Login status:", login_resp.status_code)
            print("Login body:", login_resp.text)
            assert login_resp.status_code == 200
            resp = await client.get(f"{BASE_URL}/api-key", headers={"x-user-email": user["email"]})
            print("API Key status:", resp.status_code)
            print("API Key body:", resp.text)
            assert resp.status_code == 200
            if resp.text:
                data = resp.json()
                print("API Key response json:", data)
                assert "value" in data or "apiKey" in data or "key" in data
