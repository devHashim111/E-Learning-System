import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
from apps.auth.models import User, UserRole


def extract_data(response_json):
    if isinstance(response_json, dict) and "data" in response_json:
        return response_json["data"]
    return response_json


@pytest_asyncio.fixture(scope="function")
async def client():
    async with app.router.lifespan_context(app):
        from tortoise import Tortoise

        await Tortoise.generate_schemas(safe=True)

        for model in Tortoise.apps["models"].values():
            if model.__name__ != "Aerich":
                await model.all().delete()

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            yield client


async def create_authenticated_user(
    client: AsyncClient,
    email: str,
    role: UserRole,
) -> tuple[dict[str, str], dict]:

    existing_user = await User.filter(email=email).first()
    if existing_user:
        await existing_user.delete()

    signup_res = await client.post(
        "/user/signup",
        json={
            "email": email,
            "password": "Password123!",
            "username": email.split("@")[0],
            "first_name": "Test",
            "last_name": "User",
        },
    )

    res_data = signup_res.json()
    user_data = extract_data(res_data)

    user_id = user_data.get("id") or res_data.get("id")

    if not user_id and isinstance(res_data, dict):
        for value in res_data.values():
            if isinstance(value, dict) and "id" in value:
                user_id = value["id"]
                user_data = value
                break

    assert user_id, f"Signup failed: {signup_res.status_code} {res_data}"

    user = await User.get(id=user_id)
    user.role = role
    await user.save()

    login_res = await client.post(
        "/user/login",
        json={
            "email": email,
            "password": "Password123!",
        },
    )

    assert login_res.status_code == 200, (
        f"Login failed: {login_res.status_code} {login_res.text}"
    )

    raw_login = login_res.json()
    login_data = extract_data(raw_login)

    token = (
        login_data.get("access_token")
        or raw_login.get("access_token")
        or raw_login.get("token")
    )

    assert token, f"No token returned from login: {raw_login}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    user_data["role"] = (
        role.value if hasattr(role, "value") else str(role)
    )
    user_data["id"] = str(user_id)

    return headers, user_data


@pytest_asyncio.fixture
async def supervisor_auth(client: AsyncClient):
    return await create_authenticated_user(
        client,
        "supervisor@example.com",
        UserRole.SUPERVISOR
        if hasattr(UserRole, "SUPERVISOR")
        else "supervisor",
    )


@pytest_asyncio.fixture
async def student_auth(client: AsyncClient):
    return await create_authenticated_user(
        client,
        "student@example.com",
        UserRole.STUDENT
        if hasattr(UserRole, "STUDENT")
        else "student",
    )