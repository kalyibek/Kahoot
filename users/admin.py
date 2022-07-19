from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'get_groups',
        'phone_number',
        'username',
        'rank_place',
        'final_score',
        'passed_tests_number',
    )
    list_display_links = ('id', 'first_name', 'last_name', 'username')
    search_fields = ('first_name', 'last_name')
    list_filter = ['groups']


admin.site.register(User, UserAdmin)
