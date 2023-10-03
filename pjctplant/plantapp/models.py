from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Role (models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        CUSTOMER = "CUSTOMER",'CUSTOMER'
        BOTANIST = "BOTANIST", 'BOTANIST'
        HORTICULTURE = "HORTICULTURE", 'HORTICULTURE'
    role = models.CharField(max_length=50, choices= Role.choices)