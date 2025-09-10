from rest_framework.routers import DefaultRouter
from .views import KYCCaseViewSet

router = DefaultRouter()
router.register(r"cases", KYCCaseViewSet)
urlpatterns = router.urls