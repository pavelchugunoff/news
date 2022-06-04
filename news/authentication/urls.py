from django.urls import path
from .views import AuthenticateUserAPIView, CreateUserAPIView, EditUserView, LogoutUserAPIView, RemoveUserAPIView, UserRetrieveUpdateAPIView, RegisterView, SignInView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/create/', CreateUserAPIView.as_view()),
    path('api/signin/', AuthenticateUserAPIView.as_view()),
    path('api/update/', UserRetrieveUpdateAPIView.as_view()),
    path('api/delete/', RemoveUserAPIView.as_view()),
    path('<slug:username>/edit/', EditUserView),
    path('register/', RegisterView),
    path('signin/', SignInView),
    path('logout/', LogoutUserAPIView.as_view())
]