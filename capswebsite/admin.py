from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('pk','email','date_of_inactive','is_active','is_admin','is_student','date_joined','last_login')
    search_fields = ('email',)
    readonly_fields = ('date_joined','last_login')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('is_active','is_student','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active','date_of_inactive','is_admin','is_student')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_admin','is_student'),
        }),
    )


admin.site.register(User,UserAdmin)
admin.site.unregister(Group)