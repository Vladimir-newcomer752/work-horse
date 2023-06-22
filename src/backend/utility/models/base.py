from django.contrib import admin
from django.db import models


class BaseModel(models.Model):
    def __init__(self, *args, **kwargs):
        """Base model for each other model in the application"""
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True


class BaseModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        """Base Admin model for each other model in the application"""
        super().__init__(model, admin_site)
        # If ModelAdmin ordering is missing apply the ordering of the model
        if not self.ordering:
            self.ordering = model._meta.ordering
