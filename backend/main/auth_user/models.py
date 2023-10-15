import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from nanoid import generate
from django.contrib.postgres import fields


def generate_unique_id():
    return generate(size=16)


# Create your models here.
class User(AbstractUser):
    id = models.CharField(
        primary_key=True, default=generate_unique_id, editable=False, max_length=16
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(
        max_length=100,
    )
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gol = models.CharField(max_length=100)
    nip = models.CharField(max_length=30)
    jabatan = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    no_hp = models.CharField(max_length=13)
    type = models.CharField(max_length=50, default="opd")
    role = fields.ArrayField(
        models.CharField(max_length=25, default="operator"), default=list
    )

    def __str__(self) -> str:
        return self.username + "-" + self.type

    def check_password(self, raw_password: str) -> bool:
        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()
        return hashed_password == self.password
