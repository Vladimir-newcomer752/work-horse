from django.db import OperationalError, ProgrammingError

from utility.models import Configuration


def get_configuration_bool(name: str, default: bool = None) -> bool:
    """
    Get a boolean configuration value from a Configuration object
    :param name: configuration name
    :param default: default value
    :return: configuration value
    """
    return bool(int(get_configuration_value(name=name,
                                            default=str(int(default)))))


def get_configuration_int(name: str, default: int = None) -> int:
    """
    Get an integer configuration value from a Configuration object
    :param name: configuration name
    :param default: default value
    :return: configuration value
    """
    return int(get_configuration_value(name=name,
                                       default=str(default)))


def get_configuration_value(name: str, default: str = None) -> str:
    """
    Get a configuration value from a Configuration object
    :param name: configuration name
    :param default: default value
    :return: configuration value
    """
    try:
        configuration = Configuration.objects.filter(name=name).first()
    except (OperationalError, ProgrammingError):
        configuration = None
    return configuration.value if configuration else default
