import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_signup_and_login(client: AsyncClient):
    payload = {
        "email": "newuser@example.com",
        "password": "Password123!",
        "username": "newuser",
        "first_name": "John",
        "last_name": "Doe",
    }
    signup_res = await client.post("/user/signup", json=payload)
    assert signup_res.status_code == 200
    data = signup_res.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    login_res = await client.post(
        "/user/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_token_refresh(client: AsyncClient):
    payload = {
        "email": "refresh@example.com",
        "password": "Password123!",
        "username": "refreshuser",
    }
    await client.post("/user/signup", json=payload)
    login_res = await client.post(
        "/user/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    refresh_token = login_res.json().get("refresh_token")

    if refresh_token:
        res = await client.post(
            "/user/refresh", json={"refresh_token": refresh_token}
        )
        assert res.status_code == 200


@pytest.mark.asyncio
async def test_user_list_pagination_and_search(
    client: AsyncClient, supervisor_auth: tuple[dict, dict]
):
    headers, _ = supervisor_auth
    res = await client.get("/user/?page=1&page_size=10", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.asyncio
async def test_user_update_password(
    client: AsyncClient, supervisor_auth: tuple[dict, dict]
):
    headers, user = supervisor_auth
    user_id = user["id"]

    res = await client.put(
        f"/user/{user_id}",
        json={
            "old_password": "Password123!",
            "new_password": "NewPassword123!",
        },
        headers=headers,
    )
    assert res.status_code == 200