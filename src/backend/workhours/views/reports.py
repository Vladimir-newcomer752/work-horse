import datetime
import io

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import FileResponse
from django.utils import dateformat
from django.utils.dateformat import format as format_date
from django.utils.translation import pgettext, pgettext_lazy
from django.views.generic import FormView

import xlsxwriter

from utility.constants import DATE_FORMAT_SHORT
from utility.extras import get_configuration_value, iter_dates, iter_days
from utility.mixins import RequireLoginMixin

from workhours.constants import (PERMISSION_CAN_ACCESS_REPORTS,
                                 REPORT_TEAMS_HTML,
                                 REPORT_TEAMS_XLS)
from workhours.forms import ReportForm
from workhours.mixins import TeamMixin
from workhours.models import Employee, Shift, Team


class ReportsView(RequireLoginMixin,
                  PermissionRequiredMixin,
                  TeamMixin,
                  FormView):
    permission_required = (f'workhours.{PERMISSION_CAN_ACCESS_REPORTS}', )
    template_name = 'workhours/reports/base.html'
    page_title_1 = 'Отчеты'
    form_class = ReportForm

    def form_valid(self, form):
        report_type = form.cleaned_data['report_type']
        starting_date = form.cleaned_data['starting_date']
        ending_date = form.cleaned_data['ending_date']
        if report_type == REPORT_TEAMS_HTML:
            results = self.report_teams_html(starting_date=starting_date,
                                             ending_date=ending_date)
            response = self.render_to_response(self.get_context_data(
                report_type=report_type,
                starting_date=starting_date,
                ending_date=ending_date,
                **results))
        elif report_type == REPORT_TEAMS_XLS:
            response = self.report_teams_xls(starting_date=starting_date,
                                             ending_date=ending_date)
        else:
            response = None
        return response

    def get_template_names(self):
        form = self.get_form(self.form_class)
        template_name = self.template_name
        # Change template name based on the report type
        if form.data.get('report_type') == REPORT_TEAMS_HTML:
            template_name = 'workhours/reports/teams_html.html'
        return [template_name]

    def report_teams_html(self,
                          starting_date: datetime.date,
                          ending_date: datetime.date) -> dict:
        results = []
        employees = {employee.id: (employee.first_last()
                                   if self.request.user.first_last
                                   else employee.last_first())
                     for employee
                     in Employee.objects.all()}
        for team in Team.objects.order_by('name'):
            data = {}
            notes = {}
            shifts = Shift.objects.filter(week__team=team.pk,
                                          date__gte=starting_date,
                                          date__lte=ending_date)
            # Get all the employees from the shifts and the teams
            employee_ids = set()
            for employee in team.employees.all():
                employee_ids.add(employee.pk)
            for shift in shifts.order_by().values('employee').distinct():
                employee_ids.add(shift['employee'])
            # Order employees by their names
            employee_ids = [k for k, v
                            in sorted(employees.items(),
                                      key=lambda item: item[1])
                            if k in employee_ids]
            # Get all days for each employee
            for employee in employee_ids:
                data[employee] = [None
                                  for _
                                  in iter_days(starting_date, ending_date)]
            for shift in shifts.select_related('week').order_by('date'):
                # Get relative day
                day = (shift.date - starting_date).days
                # Save shift data
                data[shift.employee_id][day] = shift
                # Save notes
                if shift.week.notes:
                    notes[shift.week.starting_date] = shift.week.notes
            results.append((team.pk, team.name, data, notes))
        return {'days': [day
                         for day
                         in iter_dates(starting_date, ending_date)],
                'employees': employees,
                'results': results}

    def report_teams_xls(self,
                         starting_date: datetime.date,
                         ending_date: datetime.date) -> dict:
        results = self.report_teams_html(starting_date=starting_date,
                                         ending_date=ending_date)
        days = results['days']
        employees = results['employees']
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        format_left = workbook.add_format({'align': 'left',
                                           'border': 1})
        format_center = workbook.add_format({'align': 'center',
                                             'border': 1})
        format_center_bold = workbook.add_format({'align': 'center',
                                                  'bold': True,
                                                  'border': 1})
        format_center_bold_middle = workbook.add_format({'align': 'center',
                                                         'valign': 'vcenter',
                                                         'bold': True,
                                                         'border': 1})
        shifts_types = (pgettext('Shift', 'Is present'),
                        pgettext('Shift', 'Is holiday'),
                        pgettext('Reports', 'Is absent'),
                        pgettext('Shift', 'Permit hours'))
        for team_id, team_name, data, notes in results['results']:
            # Add new sheet
            worksheet = workbook.add_worksheet(name=team_name)
            # Format headers
            worksheet.set_column(first_col=0,
                                 last_col=0,
                                 width=30)
            worksheet.merge_range(first_row=0,
                                  first_col=0,
                                  last_row=1,
                                  last_col=0,
                                  data=pgettext('Shift', 'Name'),
                                  cell_format=format_center_bold_middle)
            worksheet.set_column(first_col=1,
                                 last_col=1,
                                 width=20)
            worksheet.merge_range(first_row=0,
                                  first_col=1,
                                  last_row=1,
                                  last_col=1,
                                  data=pgettext('Reports', 'Type'),
                                  cell_format=format_center_bold_middle)
            worksheet.set_column(first_col=2,
                                 last_col=len(days) + 1,
                                 width=5)
            worksheet.write_row(row=0,
                                col=2,
                                data=[d.strftime('%d') for d in days],
                                cell_format=format_center_bold)
            worksheet.write_row(row=1,
                                col=2,
                                data=[dateformat.format(d, 'D') for d in days],
                                cell_format=format_center_bold)
            row_number = 2
            for employee in data:
                worksheet.merge_range(first_row=row_number,
                                      first_col=0,
                                      last_row=row_number + 3,
                                      last_col=0,
                                      data=employees[employee],
                                      cell_format=format_center_bold_middle)
                worksheet.write_column(row=row_number,
                                       col=1,
                                       data=shifts_types,
                                       cell_format=format_left)
                column_number = 2
                for shift in data[employee]:
                    shift_data = (
                        'X' if shift and shift.is_present else '',
                        'X' if shift and shift.is_holiday else '',
                        'X' if not shift or (not shift.is_present and
                                             not shift.is_holiday) else '',
                        shift.permit_hours if shift and shift.permit_hours > 0
                        else '')
                    worksheet.write_column(row=row_number,
                                           col=column_number,
                                           data=shift_data,
                                           cell_format=format_center)
                    column_number += 1
                row_number += 4
            if notes:
                date_format_short = get_configuration_value(
                    name=DATE_FORMAT_SHORT,
                    default='Y/m/d')
                format_note = workbook.add_format({'align': 'left'})
                format_note_title = workbook.add_format({'align': 'left',
                                                         'bold': True})
                row_number += 1
                worksheet.write_string(row=row_number,
                                       col=0,
                                       string='{NOTES}:'.format(
                                           NOTES=pgettext('Week', 'Notes')),
                                       cell_format=format_note_title)
                for date, note in notes.items():
                    date_end_week = date + datetime.timedelta(days=6)
                    row_number += 1
                    notes_date = '{DATE_1} - {DATE_2}'.format(
                        DATE_1=format_date(value=date,
                                           format_string=date_format_short),
                        DATE_2=format_date(value=date_end_week,
                                           format_string=date_format_short))
                    worksheet.write_string(
                        row=row_number,
                        col=0,
                        string=notes_date,
                        cell_format=format_note_title)
                    worksheet.write_string(row=row_number,
                                           col=1,
                                           string=note,
                                           cell_format=format_note)
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer,
                            as_attachment=True,
                            filename='report.xlsx')
