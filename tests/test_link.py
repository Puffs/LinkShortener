from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
import pytest_asyncio
from .utils.mock_link import mock_links


async def test_add_link(
    db_session: AsyncSession,
    client: AsyncClient,
):
    """Тест добавления ссылки."""
    response = await client.post("/api/shorten" , json={"original_link":"https://example.com//"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "short_link" in data
    assert len(data["short_link"]) == 8


async def test_redirect_to_original_link(
    db_session: AsyncSession,
    client: AsyncClient,
    mock_links: list
):
    """Тест получения счетчика ссылки."""
    response = await client.get("/api/SD4r4G72")
    assert response.status_code == status.HTTP_302_FOUND
    assert len(response.content) <= 100

async def test_get_redirect_count(
    db_session: AsyncSession,
    client: AsyncClient,
    mock_links: list
):
    """Тест получения счетчика ссылки."""
    response = await client.get("/api/stats/SD4r4G72")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "link_count" in data
    assert data["link_count"] == 0
    



    