from django import forms
from django.http import (HttpResponseForbidden,
                         HttpResponseServerError,
                         JsonResponse)
from django.views.generic import UpdateView

from utility.mixins import RequireLoginMixin

from workhours.mixins import IsInTeamUserMixin
from workhours.models import Week


class WeekCloseForm(forms.ModelForm):
    notes = forms.CharField(required=False)

    class Meta:
        model = Week
        fields = ('notes', )


class WeekCloseView(RequireLoginMixin,
                    IsInTeamUserMixin,
                    UpdateView):
    model = Week
    form_class = WeekCloseForm

    def post(self, request, *args, **kwargs):
        form = super().get_form(form_class=self.form_class)
        if form.is_valid():
            self.object = self.get_object()
            if not self.object.is_closed:
                self.object.notes = form.cleaned_data.get('notes', '')
                self.object.is_closed = True
                self.object.save()
                return JsonResponse({'code': 200})
            else:
                # The week is closed, unable to update
                return HttpResponseForbidden()
        else:
            return HttpResponseServerError()
