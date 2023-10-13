from django.db import models
from nanoid import generate


def generate_unique_id():
    return generate(size=16)


# Create your models here.
class User(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_unique_id, editable=False, max_length=16
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    type = models.CharField(max_length=255, default="opd")
    role = models.CharField(max_length=255, default="['operator']")

    def __str__(self) -> str:
        return self.username + "-" + self.type + "-" + self.role
