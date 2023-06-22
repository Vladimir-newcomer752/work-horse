import time

from django import forms
from django.http import (HttpResponseForbidden,
                         HttpResponseServerError,
                         JsonResponse)
from django.views.generic import UpdateView

from utility.extras import get_configuration_int
from utility.mixins import RequireLoginMixin

from workhours.constants import DELAY_AFTER_SAVE_SHIFT
from workhours.mixins import IsInTeamUserMixin
from workhours.models import Shift, ShiftExtra


class ShiftUpdateForm(forms.ModelForm):
    pk = forms.IntegerField(required=True)
    present = forms.BooleanField(required=False)
    holiday = forms.BooleanField(required=False)
    permit = forms.IntegerField(required=False)

    class Meta:
        model = Shift
        fields = ('pk', 'present', 'holiday', 'permit')


class ShiftUpdateView(RequireLoginMixin,
                      IsInTeamUserMixin,
                      UpdateView):
    model = Shift
    form_class = ShiftUpdateForm

    def post(self, request, *args, **kwargs):
        form = super().get_form(form_class=self.form_class)
        if form.is_valid():
            shift = Shift.objects.select_related('week', 'week__team').get(
                pk=form.cleaned_data['pk'])
            if not shift.week.is_closed:
                shift.is_present = form.cleaned_data.get('present', False)
                shift.is_holiday = form.cleaned_data.get('holiday', False)
                shift.permit_hours = form.cleaned_data.get('permit', 0)
                # Get the extras
                extras = shift.week.team.extras.filter(is_active=True).all()
                for extra in extras:
                    extra_value = form.data[f'extra_{extra.pk}']
                    if extra.type in (extra.EXTRA_TYPE_CHECK_LEFT,
                                      extra.EXTRA_TYPE_CHECK_RIGHT):
                        # Apply 1 or 0 for Checkbox values
                        extra_value = ('1'
                                       if extra_value in ('true', '1')
                                       else '0')
                    # Create a new Shift Extra or get any existing
                    shift_extra, created = ShiftExtra.objects.get_or_create(
                        shift=shift,
                        extra=extra,
                        defaults={'value': extra_value}
                    )
                    if not created and shift_extra.value != extra_value:
                        # Update existing Shift Extra
                        shift_extra.value = extra_value
                        shift_extra.save()
                    shift.extras.add(shift_extra)
                shift.save()
                # Apply a delay after saving a shift
                time.sleep(get_configuration_int(name=DELAY_AFTER_SAVE_SHIFT,
                                                 default=0) / 1000)
                return JsonResponse({'code': 200})
            else:
                # The week is closed, unable to update
                return HttpResponseForbidden()
        else:
            return HttpResponseServerError()
