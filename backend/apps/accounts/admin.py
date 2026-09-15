from django.contrib import admin

from .models import LoginAttempt


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("created_at", "username", "ip_address", "success")
    list_filter = ("success",)
    search_fields = ("username", "ip_address")
    readonly_fields = [f.name for f in LoginAttempt._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
