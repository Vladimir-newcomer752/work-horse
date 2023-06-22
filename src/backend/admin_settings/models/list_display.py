from django.db import models
from django.utils.translation import pgettext_lazy
from admin_settings.extras import get_admin_models
from utility.managers import ManagerIsActive
from utility.models.base import BaseModel, BaseModelAdmin


class ListDisplay(BaseModel):
    """List Display"""
    admin_models = get_admin_models()

    model = models.CharField(
        max_length=255,
        choices=((model_name, model_name)
                 for model_name
                 in sorted(admin_models.keys())),
        verbose_name='Модель')
    field = models.CharField(
        max_length=255,
        verbose_name='Область')
    order = models.PositiveIntegerField(
        verbose_name='Приказ')
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен')

    objects = models.Manager()
    objects_active = ManagerIsActive()

    class Meta:
        ordering = ['model', 'order', 'field']
        unique_together = (('model', 'field'),
                           ('model', 'order'))
        verbose_name = 'Отображение списка'
        verbose_name_plural = 'Отображение списка'

    def __str__(self):
        return '{MODEL} - {FIELD}'.format(MODEL=self.model,
                                          FIELD=self.field)


class ListDisplayAdmin(BaseModelAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active',)
