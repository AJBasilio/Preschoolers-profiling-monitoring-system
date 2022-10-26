import imp
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from datetime import date

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
    middle_name = models.CharField(max_length=100, null=True)
    suffix_name = models.CharField(max_length=100, default='N/A')
    phone_num = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class BarangayHealthWorker(Model):
    BARANGAYS = [('Select Barangay', 'Select Barangay'),
                 ('Burol', 'Burol'),
                 ('Burol I', 'Burol I'),
                 ('Burol II', 'Burol II'),
                 ('Burol III', 'Burol III'),
                 ('Datu Esmael', 'Datu Esmael'),
                 ('Emmanuel Begado I', 'Emmanuel Begado I'),
                 ('Emmanuel Begado II', 'Emmanuel Begado II'),]

    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    is_validated = models.BooleanField(default=False)
    bhw_barangay = models.CharField(max_length=100, choices=BARANGAYS, default='Select Barangay')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Parent(Model):
    BARANGAYS = [('Select Barangay', 'Select Barangay'),
                 ('Burol', 'Burol'),
                 ('Burol I', 'Burol I'),
                 ('Burol II', 'Burol II'),
                 ('Burol III', 'Burol III'),
                 ('Datu Esmael', 'Datu Esmael'),
                 ('Emmanuel Begado I', 'Emmanuel Begado I'),
                 ('Emmanuel Begado II', 'Emmanuel Begado II'),]

    user = models.OneToOneField(CustomUser, on_delete=CASCADE, primary_key=True)
    barangay = models.CharField(max_length=100, choices=BARANGAYS, default='Select Barangay')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Preschooler(Model):
    parent = models.ForeignKey(Parent, on_delete=CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    suffix_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def age_years(self):
        return int(date.today().year - self.birthday.year)
    
    def age_months(self):
        return int((date.today().year - self.birthday.year) * 12)

