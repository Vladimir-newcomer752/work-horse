import datetime

from django.utils.dateformat import format as format_date
from django.utils.translation import pgettext_lazy
from django.views.generic import DetailView

from utility.extras import get_configuration_int
from utility.mixins import RequireLoginMixin

from workhours.constants import WEEKS_TO_LIST
from workhours.mixins import IsInTeamUserMixin, TeamMixin
from workhours.models import Team, Week


class TeamView(RequireLoginMixin,
               TeamMixin,
               IsInTeamUserMixin,
               DetailView):
    model = Team
    template_name = 'workhours/team.html'
    page_title_1 = 'Команда'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title_1'] = self.object.name
        # Get the previous weeks
        weeks = []
        weeks_to_list = get_configuration_int(name=WEEKS_TO_LIST,
                                              default=5)
        today = datetime.date.today()
        for week_number in range(weeks_to_list):
            starting_date = (today -
                             datetime.timedelta(days=today.weekday(),
                                                weeks=week_number))
            ending_date = starting_date + datetime.timedelta(days=6)
            if week_number > 0:
                # Get a previous week if it exists
                week = Week.objects.filter(team_id=self.object.pk,
                                           starting_date=starting_date,
                                           ending_date=ending_date).first()
            else:
                # Create the current week if it's missing
                week, _ = Week.objects.get_or_create(
                    team_id=self.object.pk,
                    starting_date=starting_date,
                    ending_date=ending_date,
                    defaults={'is_closed': False})
            # Add a week if it was created or found
            if week:
                week_title = pgettext_lazy(
                    'Неделя',
                    'Неделя с {STARTING_DATE} до {ENDING_DATE}').format(
                    STARTING_DATE=format_date(
                        value=week.starting_date,
                        format_string=context['date_format_short']),
                    ENDING_DATE=format_date(
                        value=week.ending_date,
                        format_string=context['date_format_short']))
                weeks.append((week_number, week, week_title))
        context['weeks'] = weeks
        return context
