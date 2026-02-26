from rest_framework.routers import DefaultRouter
from .views import FlutterwavePaymentViewSet, PaystackPaymentViewSet, PaymentsViewSet


router = DefaultRouter()
# router.register(r'flutterwave', FlutterwavePaymentViewSet,
#                 basename='flutterwave')
# router.register(r'paystack', PaystackPaymentViewSet, basename='paystack')
router.register(r"", PaymentsViewSet, basename="payments")
urlpatterns = router.urls
