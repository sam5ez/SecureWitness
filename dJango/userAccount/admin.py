from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MainAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser', "last_login", "date_joined")
    list_editable = ('is_staff', 'is_superuser')


admin.site.unregister(User)
admin.site.register(User, MainAdmin)