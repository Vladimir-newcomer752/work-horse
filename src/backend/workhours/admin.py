from django.contrib import admin

from .models import (
    Employee, EmployeeAdmin,
    Extra, ExtraAdmin,
    Shift, ShiftAdmin,
    ShiftExtra, ShiftExtraAdmin,
    Team, TeamAdmin,
    Week, WeekAdmin
)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(ShiftExtra, ShiftExtraAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Week, WeekAdmin)
