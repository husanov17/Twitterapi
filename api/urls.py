from django.urls import path
from api.views import SendEmailRegistrationAPIView

urlpatterns = [
    path('sign-up/', SendEmailRegistrationAPIView.as_view())
]
