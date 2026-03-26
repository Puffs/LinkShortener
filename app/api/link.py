from typing import Annotated

from fastapi import APIRouter, Depends, status
from schemas import AddLinkSchema, ShortLinkOutputSchema, CountLinkOutputSchema
from fastapi.responses import RedirectResponse
from service import LinkService, get_link_service


router = APIRouter(tags=['Ссылки'])

@router.post(
    "/shorten",
    summary="Преобразовать ссылку",
    description='Принимает ссылку, возвращает короткую ссылку',
    response_model=ShortLinkOutputSchema,
)
async def save_shorter_link(
    link: AddLinkSchema,
    link_service: Annotated[LinkService, Depends(get_link_service)]
):
    short_link = await link_service.add_link(link)

    return ShortLinkOutputSchema(short_link=short_link)


@router.get(
    "/{short_id}",
    summary="Редирект на оригинальную ссылку по короткую ссылке",
    description='Принимает короткую ссылку',
)
async def redirect_to_original_link(
    short_id: str,
    link_service: Annotated[LinkService, Depends(get_link_service)]
):
    
    original_link = await link_service.get_redirect_url(short_id)

    return RedirectResponse(url=original_link, status_code=status.HTTP_302_FOUND)


@router.get(
    "/stats/{short_id}",
    summary="Получить количество переходов по ссылке",
    description='Принимает короткую ссылку',
    response_model=CountLinkOutputSchema,
)
async def get_redirect_count(
    short_id: str,
    link_service: Annotated[LinkService, Depends(get_link_service)]
):

    link_count = await link_service.get_link_count(short_id)

    return CountLinkOutputSchema(link_count=link_count)