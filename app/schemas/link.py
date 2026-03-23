from pydantic import BaseModel, AnyUrl, constr


class AddLinkSchema(BaseModel):
    """Схема ссылки."""

    original_link: AnyUrl