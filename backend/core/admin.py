from django.contrib import admin

# Register your models here.
from .models import UserLoginHistory

admin.site.register(UserLoginHistory)