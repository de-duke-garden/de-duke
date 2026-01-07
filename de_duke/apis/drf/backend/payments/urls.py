from rest_framework.routers import DefaultRouter
from .views import FlutterwavePaymentViewSet, PaystackPaymentViewSet


router = DefaultRouter()
router.register(r'flutterwave', FlutterwavePaymentViewSet,
                basename='flutterwave')
router.register(r'paystack', PaystackPaymentViewSet, basename='paystack')
urlpatterns = router.urls
