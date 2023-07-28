# authapi/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # Additional fields for the CustomUser model
    full_name = models.CharField(max_length=255)

    # You can add more fields here if needed, such as profile pictures, addresses, etc.

    class Meta:
        # Add unique related names to avoid clashes with the default User model
        swappable = 'AUTH_USER_MODEL'
        permissions = (("can_subscribe", "Can subscribe for new letters"),)

User = get_user_model()

class BlacklistedToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Token"
