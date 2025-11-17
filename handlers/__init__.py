# handlers/__init__.py — ФИНАЛЬНЫЙ И ПРАВИЛЬНЫЙ
from .start import router as start
from .games import router as games
from .profile import router as profile
from .help import router as help
from .payments import router as payments
from .admin import router as admin

__all__ = ["start", "games", "profile", "help", "payments", "admin"]
