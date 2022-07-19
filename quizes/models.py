from django.db import models
from django.contrib.auth.models import Group


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    questions_number = models.IntegerField()
    time = models.IntegerField()
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

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set')

    def __str__(self):
        return f'{self.question.text}: answer: {self.text}'


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_results_set')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class QuestionResult(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_results_set')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

