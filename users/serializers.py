from djoser.serializers import UserSerializer
from .models import User

class UserListSerializer(UserSerializer):
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


