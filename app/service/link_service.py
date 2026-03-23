from schemas.link import AddLinkSchema
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AddLinkSchema
from repository import LinkRepository
from fastapi import Depends
from db.database import get_async_session
from models import Link
import hashlib
import base62


def convert_to_shorten_url(long_url) -> str:
    hash_obj = hashlib.md5(long_url.encode())
    short_id = base62.encode(int(hash_obj.hexdigest(), 16))[:8]
    return short_id

class LinkServiceABC(ABC):
    """Интерфейс сервиса ссылки."""

    @abstractmethod
    def __init__(self, session: AsyncSession):
        """Конструктор сервиса ссылки."""
        raise NotImplementedError

    @abstractmethod
    async def add_link(self, link_data: AddLinkSchema) -> Link:
        """Добавление ссылки."""
        raise NotImplementedError
    
    @abstractmethod
    async def get_redirect_url(self, id: int) -> str:
        """Получение короткой ссылки по id."""
        raise NotImplementedError

    @abstractmethod
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки по id."""
        raise NotImplementedError


class LinkService(LinkServiceABC):
    """Сервис ссылки."""

    def __init__(self, session: AsyncSession):
        self.repository = LinkRepository(session)

    async def add_link(self, link_data: AddLinkSchema) -> Link:
        """Добавление ссылки."""

        link_dict = link_data.model_dump()
        link_dict["original_link"] = str(link_dict.get("original_link"))
        link_dict["short_link"] = convert_to_shorten_url(link_dict.get("original_link"))
        new_link = await self.repository.add_link(link_dict)
        return new_link.short_link

    async def get_redirect_url(self, short_link: str) -> str:
        """Получение оригинальной ссылки по id."""

        original_link = await self.repository.get_original_link(short_link)
        return original_link
    
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки по короткой ссылке."""

        link_count = await self.repository.get_link_count(short_link)
        return link_count


def get_link_service(
    session: AsyncSession = Depends(get_async_session),
) -> LinkService:
    return LinkService(session)