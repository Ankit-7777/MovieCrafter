from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a normal user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    """
    Custom user model that uses email as the unique identifier.
    """
    
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[6-9]\d{9}$',
                message='Enter a valid 10-digit  phone number.'
            ),
        ],
        null=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        """
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions for a given app label.
        """
        return self.is_superuser or self.is_staff

    def is_active_user(self):
        """
        Check if the user is active.
        """
        return self.is_active

