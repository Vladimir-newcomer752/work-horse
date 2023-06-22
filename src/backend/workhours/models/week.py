from django.db import models
from utility.models import BaseModel, BaseModelAdmin
from workhours.constants import PERMISSION_CAN_REOPEN_WEEKS


class Week(BaseModel):
    """
    Weeks
    """
    team = models.ForeignKey(
        to='Team',
        on_delete=models.PROTECT,
        verbose_name='Команда')
    starting_date = models.DateField(
        null=False,
        verbose_name='Дата начала')
    ending_date = models.DateField(
        null=False,
        verbose_name='Дата окончания')
    notes = models.TextField(
        blank=True,
        verbose_name='Записи')
    is_closed = models.BooleanField(
        default=False,
        verbose_name='Закрыт')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['team', 'starting_date'],
                                    name='week_unique_team_starting_date')
        ]
        ordering = ['-starting_date', '-ending_date', 'team']
        verbose_name = 'Неделя'
        verbose_name_plural = 'Неделя'
        permissions = [
            (PERMISSION_CAN_REOPEN_WEEKS, 'Can reopen weeks')
        ]

    def __str__(self):
        return '{TEAM} - {START} - {END}'.format(
            TEAM=self.team,
            START=self.starting_date.strftime('%Y-%m-%d'),
            END=self.ending_date.strftime('%Y-%m-%d'))


class WeekAdmin(BaseModelAdmin):
    list_display = ('starting_date', 'ending_date', 'team', 'is_closed')
    list_filter = ('team', 'is_closed')
