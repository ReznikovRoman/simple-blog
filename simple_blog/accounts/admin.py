from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom BaseUserAdmin for CustomUser model."""
    list_display = ('email', 'username', 'date_joined', 'is_admin',)
    search_fields = ('email', 'username',)
    readonly_fields = ('id', 'date_joined', 'last_login',)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email',),
        }),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Custom ModelAdmin for Profile model."""
    list_display = ('uplay_nickname', 'first_name', 'last_name',)
    search_fields = ('uplay_nickname',)
    readonly_fields = ('id', 'user', )
    exclude = ('USERNAME_FIELD', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()
