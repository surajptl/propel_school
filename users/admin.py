from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('full_name', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active','is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password','full_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','full_name')
    ordering = ('full_name',)

admin.site.site_header = 'Propel School'
admin.site.register(CustomUser, CustomUserAdmin)
