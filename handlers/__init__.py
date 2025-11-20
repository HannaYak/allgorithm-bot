# handlers/__init__.py — САМЫЙ ПРАВИЛЬНЫЙ ВАРИАНТ НА СВЕТЕ
from .start import router as start_router
from .games import router as games_router
from .profile import router as profile_router
from .payments import router as payments_router
from .admin import router as admin_router
from .common import router as common_router

# Теперь всё доступно как start_router, games_router и т.д.
__all__ = [
    "start_router",
    "games_router",
    "profile_router",
    "payments_router",
    "admin_router",
    "common_router"
]
