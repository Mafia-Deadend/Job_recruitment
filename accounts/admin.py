from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active','phone_number','date_joined','last_login','is_admin','is_staff','is_active','is_superadmin')
    list_display_links = ('email','first_name','last_name')

    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'first_name', 'last_name', 'password')}),
    #     ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    #     # ('Important dates', {'fields': ('last_login',)}),  # ❌ exclude 'date_joined'
    # )

    readonly_fields = ('last_login', 'date_joined')  # ✅ These are non-editable

    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'first_name', 'last_name', 'password')
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(Account, AccountAdmin)

# Register your models here.
