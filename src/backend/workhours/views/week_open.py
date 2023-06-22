from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.views.generic import DetailView

from utility.mixins import RequireLoginMixin

from workhours.constants import PERMISSION_CAN_REOPEN_WEEKS
from workhours.mixins import IsInTeamUserMixin
from workhours.models import Week


class WeekOpenView(RequireLoginMixin,
                   PermissionRequiredMixin,
                   IsInTeamUserMixin,
                   DetailView):
    model = Week
    permission_required = (f'workhours.{PERMISSION_CAN_REOPEN_WEEKS}', )

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object.is_closed = False
        self.object.save()
        return JsonResponse({'code': 200})
