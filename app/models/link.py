from uuid import uuid4
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import func, text, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_mixin import IdMixin

class Link(IdMixin, Base):
    """Модель ссылок."""

    __tablename__ = 'links'

    original_link: Mapped[str] = mapped_column(String, doc='Оригинальная ссылка', unique=True)
    short_link: Mapped[str] = mapped_column(String, doc='Краткая ссылка', unique=True)
    link_count: Mapped[int] = mapped_column(Integer, doc="Количество запросов", nullable=False, server_default=text("0"))
