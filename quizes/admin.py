from django.contrib import admin
from .models import *


class QuestionInline(admin.TabularInline):
    model = Question


class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'questions_number', 'time')


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizResult)
admin.site.register(QuestionResult)
