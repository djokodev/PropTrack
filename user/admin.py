from django.contrib import admin
from .models import UserProfile, CustomUser


admin.site.register(CustomUser)
admin.site.register(UserProfile)
