from .start import router as start_router
from .profile import router as profile_router
from .events import router as events_router
from .booking import router as booking_router
from .payments import router as payments_router
from .my_bookings import router as my_bookings_router
from .cabinet import router as cabinet_router
from .rules import router as rules_router
from .support import router as support_router
from .admin import router as admin_router

__all__ = [
    "start_router", "profile_router", "events_router", "booking_router",
    "payments_router", "my_bookings_router", "cabinet_router",
    "rules_router", "support_router", "admin_router"
]
