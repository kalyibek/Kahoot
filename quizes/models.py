from django.db import models
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError

from Kahoot import settings
from users.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="quiz_set")

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name_plural = 'Quizes'


class Question(models.Model):
    text = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_set')
    time = models.IntegerField(default=20)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()

    def get_correct_answer(self):
        return self.answer_set.get(correct=True)


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')

    def __str__(self):
        return f'{self.question.text}: answer: {self.text}'

    def save(self, *args, **kwargs):
        if Answer.objects.filter(question=self.question).count() < settings.MAX_ANSWER_COUNT:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Too many entries!')


class QuizResult(models.Model):
    score = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_result_set', null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_result', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='quiz_result_group', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.score}'


class QuestionResult(models.Model):
    score = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_result_set', null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_result', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='question_result_group', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.score}'

