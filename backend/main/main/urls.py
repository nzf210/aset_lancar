"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from auth_user import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("auth", include("auth_user.urls")),
    re_path("login", views.LoginAuthUser.as_view(), name="auth_user"),
    re_path("register", views.RegisterAuthUser.as_view(), name="register_user"),
    re_path("logout", views.LogutAuthUser.as_view(), name="logout"),
    path("refresh", views.refresh_jwt, name="refresh_jwt"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
