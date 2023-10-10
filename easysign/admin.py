from django.contrib import admin
from .models import User, Document

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'user_api_key')
    list_editable = ('user_api_key',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Document)