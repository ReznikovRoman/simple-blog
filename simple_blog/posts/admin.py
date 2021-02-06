from django.contrib import admin

from . import models


class PostAdmin(admin.ModelAdmin):
    """Custom ModelAdmin for Post model"""
    list_display = ('title', 'created_date', 'published_date')
    search_fields = ('title', )
    readonly_fields = ('created_date', 'published_date')
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()


class CommentAdmin(admin.ModelAdmin):
    """Custom ModelAdmin for Comment model"""
    list_display = ('author', 'post', 'posted_date')
    search_fields = ('author', )
    readonly_fields = ('published_date', )
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)










