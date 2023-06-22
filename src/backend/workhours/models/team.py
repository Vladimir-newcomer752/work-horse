from django.contrib.auth import get_user_model
from django.db import models
from utility.managers import ManagerIsActive
from utility.models import BaseModel, BaseModelAdmin


class Team(BaseModel):
    """
    Teams
    """
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Имя')
    description = models.TextField(
        blank=True,
        null=False,
        verbose_name='Описание')
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Активен')
    employees = models.ManyToManyField(
        to='Employee',
        verbose_name='Работники')
    managers = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        verbose_name='Менеджеры')
    extras = models.ManyToManyField(
        to='Extra',
        blank=True,
        verbose_name='Дополнительные услуги')

    # Automatically filter on the enabled only records
    objects = models.Manager()
    objects_active = ManagerIsActive()

    class Meta:
        ordering = ['name']
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name


class TeamAdmin(BaseModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
