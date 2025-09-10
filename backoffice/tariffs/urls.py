from rest_framework.routers import DefaultRouter
from .views import TariffViewSet

router = DefaultRouter()
router.register(r"", TariffViewSet)
urlpatterns = router.urls