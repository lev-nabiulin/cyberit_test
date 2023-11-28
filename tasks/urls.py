from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    TaskViewSet,
    WorkViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"works", WorkViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
