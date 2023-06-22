from django.db import models
from django.utils.translation import pgettext_lazy

from utility.models import BaseModel, BaseModelAdmin

from workhours.constants import PERMISSION_CAN_ACCESS_REPORTS


class Shift(BaseModel):
    """
    Shifts
    """
    week = models.ForeignKey(
        to='Week',
        on_delete=models.PROTECT,
        verbose_name='Неделя')
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.PROTECT,
        verbose_name='Работник')
    date = models.DateField(
        null=False,
        verbose_name='Дата')
    is_present = models.BooleanField(
        default=False,
        verbose_name='Присутствует')
    is_holiday = models.BooleanField(
        default=False,
        verbose_name='Это праздник')
    permit_hours = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Разрешенные часы')
    extras = models.ManyToManyField(
        to='ShiftExtra',
        related_name='shift_extras')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['week', 'employee', 'date'],
                                    name='shift_unique_date_employee_date')
        ]
        ordering = ['-week', '-date', 'employee']
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        permissions = [
            (PERMISSION_CAN_ACCESS_REPORTS, 'Can access reports')
        ]

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class ShiftAdmin(BaseModelAdmin):
    list_display = ('date', 'week', 'employee',
                    'is_present', 'is_holiday', 'permit_hours')
    list_filter = ('week__team', 'employee', 'week__is_closed',
                   'is_present', 'is_holiday')
