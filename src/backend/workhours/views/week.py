import datetime

from django.utils.dateformat import format as format_date
from django.utils.translation import pgettext_lazy
from django.views.generic import DetailView

from utility.extras import get_configuration_int
from utility.mixins import RequireLoginMixin

from workhours.constants import (DELAY_AFTER_SAVE_DAY,
                                 DELAY_AFTER_SAVE_WEEK,
                                 DELAY_BEFORE_SAVE_DAY,
                                 DELAY_BEFORE_SAVE_WEEK)
from workhours.mixins import IsInTeamUserMixin, TeamMixin
from workhours.models import Shift, ShiftExtra, Team, Week


class WeekView(RequireLoginMixin,
               TeamMixin,
               IsInTeamUserMixin,
               DetailView):
    model = Week
    template_name = 'workhours/week.html'
    page_title_1 = pgettext_lazy('Week', 'Week')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_format = context['date_format_short']
        context['page_title_1'] = (
            pgettext_lazy('Неделя',
                          'Неделя с {STARTING_DATE} до {ENDING_DATE}').format(
                STARTING_DATE=format_date(value=self.object.starting_date,
                                          format_string=date_format),
                ENDING_DATE=format_date(value=self.object.ending_date,
                                        format_string=date_format)))
        context['delay_after_save_day'] = get_configuration_int(
            name=DELAY_AFTER_SAVE_DAY,
            default=0
        )
        context['delay_after_save_week'] = get_configuration_int(
            name=DELAY_AFTER_SAVE_WEEK,
            default=0
        )
        context['delay_before_save_day'] = get_configuration_int(
            name=DELAY_BEFORE_SAVE_DAY,
            default=0
        )
        context['delay_before_save_week'] = get_configuration_int(
            name=DELAY_BEFORE_SAVE_WEEK,
            default=0
        )
        # Get the team employees
        team = Team.objects_active.get(pk=self.object.team_id)
        employees = team.employees.order_by(*(
            ('first_name', 'last_name')
            if self.request.user.first_last
            else ('last_name', 'first_name')))
        # Check Extras enabled for the team
        context['extras'] = team.extras.filter(is_active=True)
        # Get the days details
        days = []
        shifts_all_qs = Shift.objects.select_related('employee')
        # Get the shifts extras
        shifts_extras = ShiftExtra.objects.filter(
            shift__week=self.object).select_related('shift', 'extra')
        shifts_extras_values = {}
        for shift_extra in shifts_extras:
            if shift_extra.shift_id not in shifts_extras_values:
                shifts_extras_values[shift_extra.shift_id] = {}
            item = shifts_extras_values[shift_extra.shift_id]
            item[shift_extra.extra.name] = shift_extra.value
        # Process every day
        for day_number in range(7):
            day = (self.object.starting_date +
                   datetime.timedelta(days=day_number))
            shifts = []
            shifts_ids = []
            for employee in employees:
                shift, _ = shifts_all_qs.get_or_create(week=self.object,
                                                       employee=employee,
                                                       date=day)

                shifts.append(shift)
                shifts_ids.append(shift.pk)
            days.append((day_number, day, shifts, shifts_ids))
        context['days'] = days
        context['week_status'] = (pgettext_lazy('Week', 'Closed')
                                  if self.object.is_closed
                                  else pgettext_lazy('Week', 'Open'))
        context['shifts_extras_values'] = shifts_extras_values
        return context
