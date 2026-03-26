from schemas.link import AddLinkSchema
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AddLinkSchema
from repository import LinkRepository
from fastapi import Depends
from db.database import get_async_session
from models import Link
from exceptions import ShortUrlNotFound
from utils import convert_to_shorten_url


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
    async def get_redirect_url(self, short_link: str) -> str:
        """Получение короткой ссылки по короткой ссылке."""
        raise NotImplementedError

    @abstractmethod
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки по короткой ссылке."""
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

        link_obj = await self.repository.get_link_by_short(link_dict["short_link"])

        if link_obj is None:
            link_obj = await self.repository.add_link(link_dict)
        return link_obj.short_link

    async def get_redirect_url(self, short_link: str) -> str:
        """Получение оригинальной ссылки по короткой ссылке."""

        link_obj = await self.repository.get_link_by_short(short_link)
        if link_obj is None:
            raise ShortUrlNotFound()
        
        link_obj = await self.repository.increment_link_count(link_obj)
        
        return link_obj.link_count
    
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки по короткой ссылке."""

        link_obj = await self.repository.get_link_by_short(short_link)
        if link_obj is None:
            raise ShortUrlNotFound()
        
        return link_obj.link_count


def get_link_service(
    session: AsyncSession = Depends(get_async_session),
) -> LinkService:
    return LinkService(session)