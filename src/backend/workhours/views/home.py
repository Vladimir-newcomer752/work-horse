from django.urls import reverse_lazy
from django.views.generic import RedirectView


class HomeView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs) -> str:
        """
        Redirect page to the destination URL
        :param args:
        :param kwargs: captured arguments
        :return: destination URL
        """
        if not self.request.user.is_authenticated:
            url = reverse_lazy('workhours.auth.login',
                               kwargs=kwargs)
        else:
            page = self.request.user.login_redirect_page
            args = None
            query = None
            if page:
                if (page.startswith('/') or
                        page.startswith('http:') or
                        page.startswith('https:')):
                    # Use complete URL
                    url = page
                else:
                    # Use route with arguments and parameters
                    # Redirect page present, split page and arguments
                    if '?' in page:
                        page, query = page.split('?', 1)
                    if '/' in page:
                        page, *args = page.split('/')
                    querystring = query or ''
                    url = '{PAGE}{QUERYSTRING}'.format(
                        PAGE=reverse_lazy(page, args=args),
                        QUERYSTRING=f'?{querystring}' if querystring else '')
            else:
                url = reverse_lazy('workhours.dashboard')
        return url
