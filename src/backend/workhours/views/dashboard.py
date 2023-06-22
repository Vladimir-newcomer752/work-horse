from django.views.generic import TemplateView

from utility.mixins import RequireLoginMixin

from workhours.mixins.team import TeamMixin


class DashboardView(RequireLoginMixin,
                    TeamMixin,
                    TemplateView):
    template_name = 'workhours/dashboard.html'
    page_title_1 = 'Важная инфомация'
