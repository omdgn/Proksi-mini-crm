from fastapi import APIRouter
from app.routes import auth_route, note_route

router = APIRouter()

router.include_router(auth_route.router)
router.include_router(note_route.router)
