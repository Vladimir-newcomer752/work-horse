from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []

urlpatterns += i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include('workhours.urls')),
    prefix_default_language=True
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
