from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    final_score = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    passed_tests_number = models.PositiveIntegerField(blank=True, null=True, default=0)
    passed_tests = models.ManyToManyField('quizes.Quiz', related_name='passed_user_set', null=True)
    groups = models.ForeignKey(Group,  on_delete=models.CASCADE, related_name="user_set", null=True)

    class Meta:
        ordering = ['-passed_tests_number', '-final_score']

    def add_test(self, test):
        self.passed_tests.add(test)
        self.save()

    def set_passed_tests_number(self, number):
        self.passed_tests_number += number
        self.save()

    def set_final_score(self, score):
        self.final_score = score
        self.save()

    @staticmethod
    def calculate_final_score(quiz_results, final_score):
        results = quiz_results.aggregate(Sum('score'))['score__sum']
        if results:
            return quiz_results.aggregate(Sum('score'))['score__sum'] / quiz_results.count()
        else:
            return final_score
