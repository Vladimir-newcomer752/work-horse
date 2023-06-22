from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class RequireLoginMixin(LoginRequiredMixin):
    """
    Require user login
    """
    login_url = reverse_lazy('workhours.auth.login')
