from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Link
from exceptions import ShortUrlNotFound
from sqlalchemy.exc import IntegrityError

class LinkRepositoryABC(ABC):
    """Интерфейс для работы с ссылками."""

    @abstractmethod
    def __init__(self, session: AsyncSession):
        """Конструктор репозитория ссылки."""
        raise NotImplementedError

    @abstractmethod
    async def add_link(self, link_data: dict) -> Link:
        """Создание ссылки."""
        raise NotImplementedError

    @abstractmethod
    async def get_original_link(self, id: int) -> str:
        """Получение короткой ссылки."""
        raise NotImplementedError

    @abstractmethod
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки."""
        raise NotImplementedError


class LinkRepository(LinkRepositoryABC):
    """Репозиторий для ссылки."""

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_link(self, link_data: dict) -> Link:
        """Создание ссылки."""

        new_link = Link(**link_data)
        self.session.add(new_link)
        
        try:
            await self.session.commit()
            await self.session.refresh(new_link)
            return new_link
        except IntegrityError:
            await self.session.rollback()
            
            query = select(Link).where(Link.short_link == link_data.get("short_link"))
            result = await self.session.execute(query)
        return result.scalar_one()
    
    async def get_original_link(self, short_link: str) -> str:
        """Получение оригинальной ссылки."""

        query = select(Link).where(Link.short_link==short_link)
        result = await self.session.execute(query)
        link_obj = result.scalar_one_or_none()
        if link_obj == None:
            raise ShortUrlNotFound()
        
        link_obj.link_count += 1
        await self.session.commit()

        return link_obj.original_link
    
    async def get_link_count(self, short_link: str) -> int:
        """Получение счетчика ссылки."""

        query = select(Link.link_count).where(Link.short_link==short_link)
    
        result = await self.session.execute(query)
        result_count = result.scalar_one_or_none()
        if result_count is None:
            raise ShortUrlNotFound()

        return result_count
