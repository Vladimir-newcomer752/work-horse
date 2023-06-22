from django.db import models
from django.contrib.auth.models import AbstractUser
from utility.managers import ManagerIsActive, ManagerUser
from utility.models import BaseModel


class User(BaseModel,
           AbstractUser):
    """User"""
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name='E-mail')
    first_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Фамилия')
    login_redirect_page = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        verbose_name='Перенаправление страницы после входа в систему')
    first_last = models.BooleanField(
        choices=((True, 'Показать имя + фамилию'),
                 (False, 'Показать фамилию + имя'),
                 ),
        default=True,
        null=False,
        verbose_name='Порядок следования имени и фамилии')
    # Remove the username field with unique constraint
    username = None

    # Set the user manager
    objects = ManagerUser()
    objects_active = ManagerIsActive()

    # Set properties
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        # Define the database table
        db_table = 'auth_users'
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name()} <{self.email}>'

    def get_initials(self):
        """User initials"""
        return f'{self.first_name[0]} {self.last_name[0]}'

    def get_full_name(self):
        """User full name"""
        return f'{self.first_name} {self.last_name}'
