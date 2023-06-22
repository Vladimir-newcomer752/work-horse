from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class RequireSuperUserMixin(UserPassesTestMixin):
    """
    Require a login with superuser access
    """
    login_url = reverse_lazy('workhours.auth.login')

    def test_func(self):
        return self.request.user.is_superuser
