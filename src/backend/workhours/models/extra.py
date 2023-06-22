from django.db import models
from django.utils.translation import pgettext_lazy

from utility.managers import ManagerIsActive
from utility.models import BaseModel, BaseModelAdmin


class Extra(BaseModel):
    """
    Extras
    """
    EXTRA_TYPE_TEXT = 0
    EXTRA_TYPE_NUMERIC = 1
    EXTRA_TYPE_CHECK_LEFT = 2
    EXTRA_TYPE_CHECK_RIGHT = 3
    EXTRA_TYPE_SELECT = 4

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Имя')
    description = models.TextField(
        blank=True,
        verbose_name='Описание')
    type = models.PositiveSmallIntegerField(
        null=False,
        choices=((EXTRA_TYPE_TEXT, 'Текст'),
                 (EXTRA_TYPE_NUMERIC, 'Числовой'),
                 (EXTRA_TYPE_CHECK_LEFT, 'Флажок слева'),
                 (EXTRA_TYPE_CHECK_RIGHT, 'Флажок справа'),
                 (EXTRA_TYPE_SELECT, 'Выбрать')),
        default=True,
        verbose_name='Тип')
    minimum = models.PositiveIntegerField(
        null=False,
        default=0,
        verbose_name='Минимальное значение')
    maximum = models.PositiveIntegerField(
        null=False,
        default=0,
        verbose_name='Максимальное значение')
    values = models.TextField(
        blank=True,
        verbose_name='Значение')
    order = models.PositiveIntegerField(
        verbose_name='Приказ')
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Активен')

    objects = models.Manager()
    objects_active = ManagerIsActive()

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Дополнительный'
        verbose_name_plural = 'Дополнительные услуги'

    def __str__(self):
        return self.name


class ExtraAdmin(BaseModelAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active', )
