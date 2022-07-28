import os
from django.db import models
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError

from Kahoot import settings
from users.models import User


def images_path():
    return os.path.join(settings.MEDIA_ROOT, 'images')


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    img = models.ImageField(upload_to=images_path(), null=True)
    created = models.DateTimeField(auto_now_add=True)

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
        return f'id {self.pk}'

    def get_answers(self):
        return self.answer_set.all()

    def get_correct_answer(self):
        return self.answer_set.get(correct=True)


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')

    def __str__(self):
        return f'id {self.pk}'

    def save(self, *args, **kwargs):
        if Answer.objects.filter(question=self.question).count() < settings.MAX_ANSWER_COUNT:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Too many entries!')


class QuestionResult(models.Model):
    score = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_result_set', null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='question_result', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='question_result_answer', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='question_result_group', null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} : {self.score}'

    @staticmethod
    def calculate_score(user: User, question_id, quiz_id, answer, fact_time, submit):
        if submit:
            QuestionResult.submit_quiz(quiz_id, user)
        score = 0
        question = Question.objects.get(pk=question_id)
        quiz = Quiz.objects.get(pk=quiz_id)
        user_answer = question.answer_set.get(text=answer)
        if question.get_correct_answer().text == user_answer.text:
            if fact_time == 1:
                score = 100 - (100 / question.time * fact_time) + (100 / question.time)
            else:
                score = 100 - (100 / question.time * fact_time)

        user.set_final_score(score)
        user.set_rank_place()
        user.set_group_rank_place()

        return QuestionResult.objects.create(score=score,
                                             user=user,
                                             quiz=quiz,
                                             answer=user_answer,
                                             group=user.groups)

    @staticmethod
    def submit_quiz(quiz_id, user: User):
        quiz = Quiz.objects.get(pk=quiz_id)
        user.set_passed_tests_number(1)
        user.add_test(quiz)
