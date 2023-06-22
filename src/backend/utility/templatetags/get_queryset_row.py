##
#     Project: Django Work Hours
# Description: A Django application to manage the employees work hours
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from typing import Any

from django import template
from django.db.models import QuerySet


register = template.Library()


@register.simple_tag
def get_queryset_row(qs: QuerySet, field: str, value: Any) -> Any:
    """
    Get the first row from a queryset with matching field and value

    :param qs: Queryset with rows
    :param field: field to lookup
    :param value: field value to check
    :return: matching row from the queryset
    """
    for row in qs:
        if getattr(row, field) == value:
            return row
    return None
