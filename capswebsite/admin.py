from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import *
 
 
# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('pk','email','numberID','date_of_inactive','is_active','is_admin','is_student','has_answer','date_joined','last_login')
    search_fields = ('email','numberID','college','course','year','block',)
    readonly_fields = ('date_joined','last_login')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('is_active','is_student','is_admin','college','course','year')
    fieldsets = (
        (None, {'fields': ('email', 'password','numberID','college','course','year','block')}),
        ('Permissions', {'fields': ('is_active','date_of_inactive','is_admin','is_student','has_answer')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','numberID', 'password1', 'password2','college','course','year','block','is_admin','is_student'),
        }),
    )
 
 
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('pk','college')
    search_fields = ('pk','college',)
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('college',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk','college','course')
    search_fields = ('pk','college','course')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('college',)


admin.site.register(User,UserAdmin)
admin.site.register(College,CollegeAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Answers)
admin.site.unregister(Group)