from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django_countries.fields import CountryField
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        # if not username:
        #     raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default='admin', null=False)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()


class Countries(models.Model):
    name = models.CharField(max_length=256)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class States(models.Model):
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class BillingAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    state = models.ForeignKey(States, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)
    # country = models.ForeignKey(Countries, on_delete=models.RESTRICT)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100, null=True)
    to_use = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    # def clean(self):
    #     self.is_cleaned = True
    #     if self.state.country.id != self.country.id:
    #         raise ValidationError(_("This state cannot be found in this country"))
    #     super().clean()
    #
    # def save(self, *args, **kwargs):
    #     if not self.is_cleaned:
    #         self.full_clean()
    #     super().save(*args, **kwargs)

