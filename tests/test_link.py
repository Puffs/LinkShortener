from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from .utils.mock_link import mock_links


async def test_save_shorter_link(
    db_session: AsyncSession,
    client: AsyncClient,
):
    """Тест добавления ссылки."""
    response = await client.post("/api/shorten" , json={"original_link":"https://example.com"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "short_link" in data
    assert len(data["short_link"]) == 8


async def test_save_exist_shorter_link(
    db_session: AsyncSession,
    client: AsyncClient,
    mock_links: list
):
    """Тест добавления ссылки."""
    response = await client.post("/api/shorten" , json={"original_link":"https://fastapi.tiangolo.com"})
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


async def test_failed_redirect_to_original_link(
    db_session: AsyncSession,
    client: AsyncClient,
    mock_links: list
):
    """Тест получения счетчика ссылки."""
    response = await client.get("/api/wwwww")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert isinstance(data, dict)
    assert data.get("detail") == "Ссылка не найдена"


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


async def test_failed_get_redirect_count(
    db_session: AsyncSession,
    client: AsyncClient,
    mock_links: list
):
    """Тест получения счетчика ссылки."""
    response = await client.get("/api/stats/wwww")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert isinstance(data, dict)
    assert data.get("detail") == "Ссылка не найдена"
    



    