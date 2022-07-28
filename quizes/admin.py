from django.contrib import admin
from .models import *
from nested_inline.admin import NestedModelAdmin, NestedStackedInline


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 0
    fields = ('text', 'correct')
    readonly_fields = ('text', 'correct')

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False


class QuestionInline(NestedStackedInline):
    inlines = [AnswerInline]
    model = Question
    extra = 0
    fields = ['text']
    readonly_fields = ['text']

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False


class AnswerAdmin(NestedModelAdmin):
    list_display = ('id', 'text', 'correct', 'question')

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAdmin(NestedModelAdmin):
    inlines = [AnswerInline]
    list_display = ('id', 'text', 'time', 'quiz')

    # def has_add_permission(self, request):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'questions_number', 'passed_users_number')

    @staticmethod
    def questions_number(obj: Quiz):
        return obj.get_questions().count()

    @staticmethod
    def passed_users_number(obj: Quiz):
        result = User.objects.filter(passed_tests=obj)
        return result.count()

    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionResult)
