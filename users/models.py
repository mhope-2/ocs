from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

class Role(models.Model):
    role = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.role) 


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=140,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        )
    )
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    last_logout = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)    

    def __str__(self):
        return "{} | {} | {}".format(self.id, self.email, self.role) 

