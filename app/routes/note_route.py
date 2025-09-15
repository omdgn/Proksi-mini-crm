from fastapi import APIRouter
from app.controllers import note_controller

router = APIRouter()
router.include_router(note_controller.router)
