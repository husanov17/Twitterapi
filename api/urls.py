from django.urls import path
from api.views import SendEmailRegistrationAPIView, CodeVerifyAPIView, ResendCodeAPIView, FullSignUpAPIView, LoginAPIView, CreatePostAPIView, UpdateDeleteAPIView, CreateMediaAPIView, DeleteMediaAPIView
    

urlpatterns = [
    # Auth
    path('sign-up/', SendEmailRegistrationAPIView.as_view()),
    path('verify/', CodeVerifyAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('full-signup/', FullSignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    
    #post
    path("post/", CreatePostAPIView.as_view()),
    path("update-delete/<int:pk>/", UpdateDeleteAPIView.as_view()),
    path("media/", CreateMediaAPIView.as_view()),
    path("delete-media/<int:pk>/", DeleteMediaAPIView.as_view()),
]