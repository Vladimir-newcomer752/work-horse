from django.contrib.auth.mixins import UserPassesTestMixin
from workhours.models import Shift, Team, Week


class IsInTeamUserMixin(UserPassesTestMixin):
    """
    Check if the current user belongs to the team
    Applies to Team, Week and Shift objects
    """
    def test_func(self):
        # Get the object ID from arguments
        object_id = self.kwargs.get('pk')
        if not object_id:
            # Check if there's a valid form
            form = super().get_form(form_class=self.form_class)
            if form.is_valid():
                object_id = form.cleaned_data['pk']
        result = False
        if issubclass(self.model, Team):
            # Check team
            record = self.model.objects.get(pk=object_id)
            result = self.request.user in record.managers.all()
        elif issubclass(self.model, Week):
            # Check week
            record = self.model.objects.get(pk=object_id)
            result = self.request.user in record.team.managers.all()
        elif issubclass(self.model, Shift):
            # Check shift
            record = self.model.objects.get(pk=object_id)
            result = self.request.user in record.week.team.managers.all()
        return result
