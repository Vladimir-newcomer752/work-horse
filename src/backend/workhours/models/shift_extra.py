from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin


class ShiftExtra(BaseModel):
    """
    Shift Extras
    """
    shift = models.ForeignKey(
        to='Shift',
        on_delete=models.PROTECT,
        verbose_name='Изменение')
    extra = models.ForeignKey(
        to='Extra',
        on_delete=models.PROTECT,
        verbose_name='Дополнительный')
    value = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        verbose_name='Ценность')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['shift', 'extra'],
                                    name='shiftextra_unique_shift_extra')
        ]
        ordering = ['-shift', 'extra']
        verbose_name = 'Дополнительная смена'
        verbose_name_plural = 'Дополнительные смены'

    def __str__(self):
        return f'{self.shift} {self.extra.name}'

    def employee(self):
        return self.shift.employee

    def team(self):
        return self.shift.week.team


class ShiftExtraAdmin(BaseModelAdmin):
    list_display = ('shift', 'employee', 'extra')
    list_filter = ('shift__week__team', 'shift__employee',
                   'extra', 'extra__type')
