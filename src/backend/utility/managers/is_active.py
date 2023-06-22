from django.db import models


class ManagerIsActive(models.Manager):
    """
    Filter the data with the is_active status only
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
