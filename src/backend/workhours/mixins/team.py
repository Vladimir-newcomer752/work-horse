from utility.mixins import GenericMixin
from workhours.models import Team


class TeamMixin(GenericMixin):
    """Team mixin"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add team objects
        context['teams'] = Team.objects_active.filter(
            managers__id=self.request.user.pk)
        return context
