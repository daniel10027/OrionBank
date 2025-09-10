from rest_framework.routers import DefaultRouter
from .views import DisputeViewSet

router = DefaultRouter()
router.register(r"cases", DisputeViewSet)
urlpatterns = router.urls