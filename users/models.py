from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    final_score = models.FloatField(blank=True, null=True, default=0)
    passed_tests_number = models.PositiveIntegerField(blank=True, null=True, default=0)
    passed_tests = models.ManyToManyField('quizes.Quiz', related_name='passed_user_set', null=True, blank=True)
    groups = models.ForeignKey(Group,  on_delete=models.CASCADE, related_name="user_set", null=True, blank=True)
    rank_place = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    group_rank_place = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['rank_place']

    def add_test(self, test):
        self.passed_tests.add(test)
        self.save()

    def set_passed_tests_number(self, number):
        self.passed_tests_number += number
        self.save()

    def set_final_score(self, score):
        self.final_score += score
        self.save()

    @staticmethod
    def set_rank_place():
        users = User.objects.all().order_by('-final_score')
        for i in range(len(users)):
            users[i].rank_place = i + 1
            users[i].save()

    def set_group_rank_place(self):
        users = User.objects.filter(groups=self.groups).order_by('-final_score')
        for i in range(len(users)):
            users[i].group_rank_place = i + 1
            users[i].save()
