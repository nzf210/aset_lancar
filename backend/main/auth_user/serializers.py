from django.forms import ValidationError
from rest_framework import serializers
from .models import User
import re


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "created_at",
            "updated_at",
            "type",
            "role",
        )
