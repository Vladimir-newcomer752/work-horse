import datetime

from django import forms
from django.utils.translation import pgettext_lazy

from bootstrap_datepicker_plus.widgets import DatePickerInput

from workhours.constants import REPORT_TEAMS_HTML, REPORT_TEAMS_XLS


class ReportForm(forms.Form):
    report_type = forms.ChoiceField(
        choices=[(REPORT_TEAMS_HTML,
                  pgettext_lazy('Отчеты', 'Команды в HTML')),
                 (REPORT_TEAMS_XLS,
                  pgettext_lazy('Отчеты', 'Команды в Excel')),
                 ],
        required=True,
        label=pgettext_lazy('Отчеты', 'Тип отчета'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    starting_date = forms.DateField(
        required=True,
        label=pgettext_lazy('Отчеты', 'Дата начала'),
        widget=DatePickerInput(format='%Y/%m/%d',
                               options={'showClose': False,
                                        'showClear': False,
                                        'showTodayButton': True
                                        }),
        initial=datetime.date.today().strftime('%Y/%m/%d'))
    ending_date = forms.DateField(
        required=True,
        label=pgettext_lazy('Отчеты', 'Дата окончания'),
        widget=DatePickerInput(format='%Y/%m/%d',
                               options={'showClose': False,
                                        'showClear': False,
                                        'showTodayButton': True
                                        }),
        initial=datetime.date.today().strftime('%Y/%m/%d'))
