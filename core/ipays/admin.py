from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'avatar', 'wallpaper', 'level', 'fullname', 
        'birthday', 'adr_tinh', 'adr_huyen', 'adr_xa', 
        'adr_details', 'adr_full', 'phone', 'zalo_key', 
        'zalo_name', 'sologan', 'created', 'updated'
    )
    list_filter = ('level', 'birthday', 'created', 'updated')
    search_fields = ('user__username', 'fullname', 'phone', 'zalo_key', 'zalo_name')
    readonly_fields = ('created', 'updated')
    ordering = ('-created',)

@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'img_tag', 
        'user', 'Comment', 'created', 'updated')
    search_fields = ('file_name', 'file_type', 'user__username', 'Comment')
    list_filter = ('file_type', 'created', 'updated')
    readonly_fields = ('img_tag', 'created', 'updated')
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('img_tag',)
        return self.readonly_fields