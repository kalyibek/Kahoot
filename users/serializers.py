from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'groups',
            'phone_number',
            'username',
            'rank_place',
            'final_score',
            'passed_tests_number',
        ]

