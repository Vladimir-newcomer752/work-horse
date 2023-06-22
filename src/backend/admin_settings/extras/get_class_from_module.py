import importlib


def get_class_from_module(module_class):
    """Get Class from a module"""
    module_name, class_name = module_class.rsplit('.', 1)
    return getattr(importlib.import_module(module_name), class_name)
