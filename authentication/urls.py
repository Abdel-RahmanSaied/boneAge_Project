from .views import *
from rest_framework import routers
from django.urls import path
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("login/", CustomAuthToken.as_view()),
    ]

urlpatterns += router.urls
