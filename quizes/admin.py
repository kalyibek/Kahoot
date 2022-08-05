from django.contrib import admin
from .models import *
import nested_admin

class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    extra = 4
    max_num = 4

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionInline(nested_admin.NestedStackedInline):
    inlines = [AnswerInline]
    model = Question

    def has_delete_permission(self, request, obj=None):
        return False


class AnswerAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'text', 'correct', 'question')

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [AnswerInline]
    list_display = ('id', 'text', 'time', 'quiz')

    def has_delete_permission(self, request, obj=None):
        return False


class QuizAdmin(nested_admin.NestedModelAdmin):
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
