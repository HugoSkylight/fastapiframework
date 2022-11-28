from fastapi import APIRouter

from fast_framework.example.api.user import UserResource

router = APIRouter()

router.include_router(router=UserResource().as_router())