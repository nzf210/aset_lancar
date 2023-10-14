import hashlib
from django.forms import ValidationError
from rest_framework import serializers
from .models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "email",
            "type",
            "role",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        validated_data["password"] = hashed_password
        user = User.objects.create(**validated_data)
        return user


class AuthUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    avatar = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "email",
            "created_at",
            "updated_at",
            "type",
            "role",
        )
