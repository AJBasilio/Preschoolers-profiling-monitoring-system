from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = [('Choose User Type', 'Choose User Type'),
                 ('Admin', 'Administrator'),
                 ('BHW', 'Barangay Health Worker'),
                 ('P/G', 'Parent/Guardian')]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPE, default='Choose User Type')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class BarangayHealthWorker(Model):
    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        

class Parents(Model):
    pass