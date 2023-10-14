import re
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from .models import User
from .serializers import AuthUserSerializer, AuthUserUpdateSerializer
import hashlib
from .utils.jwt import TokenManager
from .utils.validate_req_jwt import validate_access_token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


def validate_email(value: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, value):
        return False
    else:
        return True


def validate_email_username(value: str) -> str:
    user = (
        User.objects.filter(
            username=value,
        )
        .exclude(username=value)
        .exists()
    )
    print(user)
    if user:
        return "username"
    email = (
        User.objects.filter(
            email=value,
        )
        .exclude(email=value)
        .exists()
    )
    print(email)
    if email or validate_email(value):
        return "email"
    return ""


@api_view(["GET", "POST"])
@validate_access_token
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid pk"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AuthUserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "PUT":
        serializer = AuthUserUpdateSerializer(user, data=request.data)

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
            is_password = request.data.get("password")
            if is_password:
                password = serializer.validated_data.get("password")
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                serializer.save(password=hashed_password)
            else:
                serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user.delete()
        return JsonResponse(
            {"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class RegisterAuthUser(APIView):
    def post(self, request):
        serializer = AuthUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAuthUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(
            username=username,
        ).first()

        if not user or not user.check_password(raw_password=password):
            raise AuthenticationFailed("pengguna atau password salah")

        payload = {"id": user.id}
        access_token = TokenManager().generate_token(payload=payload)
        refresh_token = TokenManager().refresh_token(token=access_token)
        response = Response()
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        response.data = {
            "jwt": access_token,
        }

        return response


class LogutAuthUser(APIView):
    def post(self, request):
        response = Response()
        response.set_cookie(key="access_token", value="", httponly=True)
        response.set_cookie(key="refresh_token", value="", httponly=True)

        response.data = {
            "access_token": "",
        }
        return response


# @api_view(["POST"])
# def auth_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     try:
#         user = User.objects.filter(
#             username=username,
#         )
#     except User.DoesNotExist:
#         return JsonResponse(
#             {"error": "Username or password missing."}, status=status.HTTP_404_NOT_FOUND
#         )

#     try:
#         if not username or not password:
#             return JsonResponse(
#                 {"message": "Username or password missing"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         serializer = AuthUserSerializer(user, many=True)
#         hashed_password = hashlib.sha256(password.encode()).hexdigest()
#         serialized_data = serializer.data
#         password_from_serializer = serialized_data[0].get("password")
#         print(password_from_serializer, hashed_password)
#         if password_from_serializer == hashed_password:
#             token_jwt = TokenManager().generate_token(
#                 payload=serialized_data[0],
#             )
#             refresh_jwt = TokenManager().refresh_token(token_jwt)
#             HttpResponse.set_cookie(key="access_token", value=token_jwt, httponly=True)
#             return JsonResponse(
#                 {"access_token": token_jwt, "refresh_token": refresh_jwt},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return JsonResponse(
#                 {"message": "User or password invalid."}, status=status.HTTP_200_OK
#             )
#     except User.DoesNotExist:
#         return JsonResponse(
#             {"message": "User or password invalid"}, status=status.HTTP_200_OK
#         )


@api_view(["GET"])
def refresh_jwt(request):
    try:
        token = request.GET.get("token")  # Get the value of the "token" query parameter
        if not token:
            return JsonResponse(
                {"message": "Please provide a token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token_jwt = TokenManager().refresh_token(token=token)
        return JsonResponse({"refresh_token": token_jwt}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "User or password invalid"}, status=status.HTTP_200_OK
        )
