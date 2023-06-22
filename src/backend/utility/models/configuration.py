from django.db import models
from django.utils.translation import pgettext_lazy
from .base import BaseModel, BaseModelAdmin


class Configuration(BaseModel):
    """Configuration item"""
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='Имя')
    group = models.CharField(
        max_length=255,
        default='',
        blank=False,
        null=False,
        verbose_name='Группа')
    value = models.TextField(
        blank=True,
        null=False,
        verbose_name='Значение')
    description = models.TextField(
        blank=True,
        verbose_name='Описание')

    class Meta:
        # Define the database table
        ordering = ['group', 'name']
        verbose_name = 'Конфигурация'
        verbose_name_plural = 'Конфигурации'

    def __str__(self):
        return self.name


class ConfigurationAdmin(BaseModelAdmin):
    list_display = ('name', 'group')
    list_filter = ('group', )
