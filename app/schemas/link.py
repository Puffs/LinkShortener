from pydantic import BaseModel, AnyUrl


class BaseLinkSchema(BaseModel):
    "Базовая схема ссылки"
    id: int


class AddLinkSchema(BaseModel):
    """Схема ссылки."""

    original_link: AnyUrl


class ShortLinkOutputSchema(BaseModel):
    """Схема ссылки."""

    short_link: str

class CountLinkOutputSchema(BaseModel):
    """Схема ссылки."""

    link_count: int