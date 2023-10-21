from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=0)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"