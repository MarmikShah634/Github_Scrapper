from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, UserLinks

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserLinks)
class UserLinksAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'created_at')
    search_fields = ('url', 'user__username', 'user__email')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
