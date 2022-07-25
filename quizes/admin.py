from django.contrib import admin
from .models import *
from nested_inline.admin import NestedModelAdmin, NestedStackedInline


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 0


class QuestionAdmin(NestedModelAdmin):
    inlines = [AnswerInline]


class QuestionInline(NestedStackedInline):
    inlines = [AnswerInline]
    model = Question
    extra = 0


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


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizResult)
admin.site.register(QuestionResult)
