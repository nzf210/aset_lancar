import re
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializers import AuthUserSerializer
import hashlib


def validate_email(value: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, value):
        return False
    else:
        return True


def validate_email_username(value: str) -> str:
    user = User.objects.filter(
        username=value,
    )
    print(user)
    if user:
        return "username"
    email = User.objects.filter(
        email=value,
    )
    print(email)
    if email or validate_email(value):
        return "email"
    return ""


@api_view(["GET", "POST"])
def get_users(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = AuthUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        serializer = AuthUserSerializer(data=request.data)
        if validate_email_username(request.data.get("username")) == "username":
            return JsonResponse(
                {"message": "Invalid username or already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if validate_email_username(request.data.get("email")) == "email":
            return JsonResponse(
                {"message": "Invalid email or already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            password = serializer.validated_data.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            serializer.save(password=hashed_password)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            {"message": "Invalid email or password", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
def get_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid pk"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AuthUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "PUT":
        serializer = AuthUserSerializer(user, data=request.data)

        if validate_email_username(request.data.get("username")) == "username":
            return JsonResponse(
                {"message": "Invalid username or already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if validate_email_username(request.data.get("email")) == "email":
            return JsonResponse(
                {"message": "Invalid email or already exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user.delete()
        return JsonResponse(
            {"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT
        )
