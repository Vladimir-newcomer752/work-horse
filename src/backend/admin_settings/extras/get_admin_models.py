from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.forms.widgets import MediaDefiningClass


def get_admin_models():
    """Get all the ModelAdmin in every loaded application"""
    admin_models = {}
    for application in apps.app_configs.keys():
        application_module = apps.app_configs[application]
        application_module.import_models()
        for module_name in dir(application_module.models_module):
            obj = getattr(application_module.models_module, module_name)
            if (issubclass(obj.__class__, MediaDefiningClass) and
                    issubclass(obj, admin.options.BaseModelAdmin) and
                    # Avoid to list the BaseModelAdmin class
                    obj.__name__ not in 'BaseModelAdmin'):
                admin_models[obj.__name__] = obj
    # Add dummy models from ADMIN_MODELS_REFERENCING_MODELS_WITH_CHOICES
    for obj in settings.ADMIN_MODELS_REFERENCING_MODELS_WITH_CHOICES:
        if obj not in admin_models:
            admin_models[obj] = None
    return admin_models
