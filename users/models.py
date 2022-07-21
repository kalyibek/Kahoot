from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    rank_place = models.PositiveIntegerField(blank=True, null=True)
    final_score = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    passed_tests_number = models.PositiveIntegerField(blank=True, null=True)
    groups = models.ForeignKey(Group,  on_delete=models.CASCADE, related_name="user_set", null=True)

    class Meta:
        ordering = ['rank_place']


