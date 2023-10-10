from django.contrib import admin
from .models import Document
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'user_api_key')
    list_editable = ('user_api_key',)

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Document)