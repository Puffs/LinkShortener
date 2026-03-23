from fastapi import APIRouter
from .link import router as link_routers


router = APIRouter(
    prefix='/api'
)

router.include_router(link_routers)