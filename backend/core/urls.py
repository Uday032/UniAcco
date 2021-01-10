from django.urls import path
from .views import current_user, UserList, UserLogin, GoogleLogin, CurrentUser, UserProfileViewSet

urlpatterns = [
    path('current_user/', CurrentUser.as_view()),
    path('users/', UserList.as_view()),
    path('loginuser/', UserLogin.as_view()),
    path('googlelogin/', GoogleLogin.as_view()),
    path('setprofile/', UserProfileViewSet.as_view())
]