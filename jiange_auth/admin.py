#coding:utf-8
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from jiange_auth.models import jiangeUser
from jiange_auth.forms import jiangeUserCreationForm

# Register your models here.

class jiangeUserAdmin(UserAdmin):
    add_form = jiangeUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email' , 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (u'基本信息', {'fields': ('username', 'password','email')}),
        (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (u'时间信息', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
admin.site.register(jiangeUser,jiangeUserAdmin)
