from django.urls import path
from .views import current_user, UserList, UserLogin

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('loginuser/', UserLogin.as_view())
]