from rest_framework.routers import DefaultRouter
from app.views import *

router = DefaultRouter()

router.register(r"filter", OrderFilterView, basename='filter')
router.register(r"order", OrderView, basename='order')
router.register(r"passanger", PassangerView, basename='passanger')
# router.register(r"status", PassangerStatusView, basename="status")
