from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        User = get_user_model()
        users = User.objects.filter(email=data['email'])
        if not users:
            raise serializers.ValidationError("Incorrect Credentials")

        for user_obj in users:
            user = authenticate(username=user_obj.username, password=data['password'])
            if user and user.is_active:
                return user
        raise serializers.ValidationError("Incorrect Credentials")
