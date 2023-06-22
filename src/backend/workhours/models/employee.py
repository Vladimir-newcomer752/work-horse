from django.db import models
from django.utils.translation import pgettext_lazy
from admin_settings.text_input_filter import TextInputFilter
from utility.managers import ManagerIsActive
from utility.models import BaseModel, BaseModelAdmin


class EmployeeFirstNameFilter(TextInputFilter):
    parameter_name = 'first_name'
    title = 'Имя'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_name__icontains=self.value())


class EmployeeLastNameFilter(TextInputFilter):
    parameter_name = 'last_name'
    title = 'Фамилия'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(last_name__icontains=self.value())


class Employee(BaseModel):
    """
    Employees
    """
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
    is_active = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Активен')

    objects = models.Manager()
    objects_active = ManagerIsActive()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'],
                                    name='employee_unique_first_last_name')
        ]
        ordering = ['first_name', 'last_name']
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.first_last()

    def first_last(self):
        return f'{self.first_name} {self.last_name}'

    def last_first(self):
        return f'{self.last_name} {self.first_name}'


class EmployeeAdmin(BaseModelAdmin):
    list_display = ('__str__', 'is_active')
    list_filter = ('is_active', )
