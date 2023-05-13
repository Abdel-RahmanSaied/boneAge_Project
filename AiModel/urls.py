from rest_framework.routers import DefaultRouter
from .views import XrayViewSet

router = DefaultRouter()
router.register(r'xray', XrayViewSet, basename='xray')

urlpatterns = router.urls