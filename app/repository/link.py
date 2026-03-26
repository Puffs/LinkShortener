from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Link


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
    async def get_link_by_short(self, short_link: str) -> Link:
        """Получение оригинальной ссылки по короткой ссылке."""
        raise NotImplementedError

    @abstractmethod
    async def increment_link_count(self, link_obj: Link) -> Link:
        """Увеличение счетчика перехода по ссылке на 1"""
        raise NotImplementedError

class LinkRepository(LinkRepositoryABC):
    """Репозиторий для ссылки."""

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_link(self, link_data: dict) -> Link:
        """Создание ссылки."""

        new_link = Link(**link_data)
        self.session.add(new_link)
        await self.session.commit()
        await self.session.refresh(new_link)

        return new_link
    
    async def get_link_by_short(self, short_link: str) -> Link:
        """Получение оригинальной ссылки по короткой ссылке."""

        query = select(Link).where(Link.short_link==short_link)
        result = await self.session.execute(query)
        link_obj = result.scalar_one_or_none()

        return link_obj

    async def increment_link_count(self, link_obj: Link) -> Link:
        """Увеличение счетчика перехода по ссылке на 1"""

        link_obj.link_count += 1
        self.session.add(link_obj)
        await self.session.commit()
        await self.session.refresh(link_obj)
        
        return link_obj