from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

USER = 'user'
ADMIN = 'admin'

CHOICES = (
    (USER, 'user'),
    (ADMIN, 'admin')
)


class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name, role):
        user = self.model(username=username, email=email,
                          password=password, first_name=first_name, last_name=last_name, role=role)
        user.is_superuser = False
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role='admin'):
        user = self.model(username=username, email=email,
                          password=password)
        user.set_password(password)
        user.is_staff = True
        user.role = 'admin'
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        return self.get(username=username_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        max_length=254, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=254, blank=True,
                            choices=CHOICES, default='user')
    password = models.CharField(
        max_length=128,
        blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, null=False)
    is_subscribed = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.username

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
