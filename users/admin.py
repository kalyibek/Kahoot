from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline
from .models import *
from quizes.models import *


class QuestionResultInline(NestedStackedInline):
    model = QuestionResult
    extra = 0


class QuizResultInline(NestedStackedInline):
    model = QuizResult
    inlines = [QuestionResultInline]
    extra = 0


class UserAdmin(NestedModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'groups',
        'phone_number',
        'username',
        'final_score',
        'passed_tests_number',
        'rank_place',
        'group_rank_place',
    )
    list_display_links = ('id', 'first_name', 'last_name', 'username')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ['groups']
    inlines = [QuestionResultInline]

admin.site.register(User, UserAdmin)
