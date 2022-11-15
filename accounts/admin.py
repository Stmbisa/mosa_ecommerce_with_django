from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccounAdmin(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'username', 'last_login','date_joined','is_active' )
    list_display_links = ('email','first_name', 'last_name', 'username', )
    readonly_fields= ('date_joined','last_login' )
    ordering = ('-date_joined',)

    filter_horizontal=()
    list_filter = ()
    fieldsets= ()
admin.site.register(Account, AccounAdmin)
