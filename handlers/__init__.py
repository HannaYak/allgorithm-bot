from .start import router as start_router
from .games import router as games_router
from .profile import router as profile_router
from .help import router as help_router
from .payments import router as payments_router
from .admin import router as admin_router

start = start_router
games = games_router
profile = profile_router
help = help_router
payments = payments_router
admin = admin_router

__all__ = ["start", "games", "profile", "help", "payments", "admin"]
