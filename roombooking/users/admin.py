from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'department', 'position', 'employee_id', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('department', 'position', 'employee_id', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'department', 'position', 'employee_id', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'department', 'employee_id')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

