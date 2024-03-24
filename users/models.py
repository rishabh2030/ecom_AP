from django.db import models
from helper.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the provided email and password.

        :param email: The email address of the user.
        :param password: The password for the user. If not provided, a random password is generated.
        :param extra_fields: Additional fields to be included in the user model.
        :raises ValueError: If the email field is not provided.
        :return: The newly created user.
        """
        if not email :
            raise ValueError("Email filed must be set")
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self,email,password=None,**extra_fields):
        """
        Creates and saves a new superuser with the provided email and password.

        :param email: The email address of the superuser.
        :param password: The password for the superuser. If not provided, a random password is generated.
        :param extra_fields: Additional fields to be included in the superuser model.
        :raises ValueError: If is_staff or is_superuser is not explicitly set to True.
        :return: The newly created superuser.
        """

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin,BaseModel):
    """
    Custom user model representing a user in the system.

    Inherits from AbstractBaseUser and PermissionsMixin for custom user authentication and permissions handling.
    Inherits BaseModel from helper for adding common fields.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def get_tokens(self):
        """Returns a tuple of JWT tokens (token, refresh_token)"""
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token), str(refresh)
    
    def __str__(self) :
        return f'{self.name}'