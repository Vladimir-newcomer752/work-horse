from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView as DjangoLogoutView

from utility.mixins import GenericMixin


class LogoutView(GenericMixin,
                 DjangoLogoutView):
    next_page = reverse_lazy('workhours.auth.login')
