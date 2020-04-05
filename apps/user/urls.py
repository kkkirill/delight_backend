from django.urls import path

from apps.user.views.user import (
    UserGetDetailsView, UserLoginView, UserLogoutView, UserRegistrationView)

urlpatterns = [
    path('registration/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('me/', UserGetDetailsView.as_view()),
]
