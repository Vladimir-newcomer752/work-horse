# Generated by Django 4.0.5 on 2023-05-30 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workhours', '0001_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Имя')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Текст'), (1, 'Числовой'), (2, 'Флажок слева'), (3, 'Флажок справа'), (4, 'Выбрать')], default=True, verbose_name='Тип')),
                ('minimum', models.PositiveIntegerField(default=0, verbose_name='Минимальное значение')),
                ('maximum', models.PositiveIntegerField(default=0, verbose_name='Максимальное значение')),
                ('values', models.TextField(blank=True, verbose_name='Значение')),
                ('order', models.PositiveIntegerField(verbose_name='Приказ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Дополнительный',
                'verbose_name_plural': 'Дополнительные услуги',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('is_present', models.BooleanField(default=False, verbose_name='Присутствует')),
                ('is_holiday', models.BooleanField(default=False, verbose_name='Это праздник')),
                ('permit_hours', models.PositiveSmallIntegerField(default=0, verbose_name='Разрешенные часы')),
            ],
            options={
                'verbose_name': 'Смена',
                'verbose_name_plural': 'Смены',
                'ordering': ['-week', '-date', 'employee'],
                'permissions': [('can_access_reports', 'Can access reports')],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Имя')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'Работник', 'verbose_name_plural': 'Работники'},
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Фамилия'),
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_date', models.DateField(verbose_name='Дата начала')),
                ('ending_date', models.DateField(verbose_name='Дата окончания')),
                ('notes', models.TextField(blank=True, verbose_name='Записи')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Закрыт')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workhours.team', verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Неделя',
                'verbose_name_plural': 'Неделя',
                'ordering': ['-starting_date', '-ending_date', 'team'],
                'permissions': [('can_reopen_weeks', 'Can reopen weeks')],
            },
        ),
        migrations.AddField(
            model_name='team',
            name='employees',
            field=models.ManyToManyField(to='workhours.employee', verbose_name='Работники'),
        ),
        migrations.AddField(
            model_name='team',
            name='extras',
            field=models.ManyToManyField(blank=True, to='workhours.extra', verbose_name='Дополнительные услуги'),
        ),
        migrations.AddField(
            model_name='team',
            name='managers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Менеджеры'),
        ),
        migrations.CreateModel(
            name='ShiftExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=255, verbose_name='Ценность')),
                ('extra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workhours.extra', verbose_name='Дополнительный')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workhours.shift', verbose_name='Изменение')),
            ],
            options={
                'verbose_name': 'Дополнительная смена',
                'verbose_name_plural': 'Дополнительные смены',
                'ordering': ['-shift', 'extra'],
            },
        ),
        migrations.AddField(
            model_name='shift',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workhours.employee', verbose_name='Работник'),
        ),
        migrations.AddField(
            model_name='shift',
            name='extras',
            field=models.ManyToManyField(related_name='shift_extras', to='workhours.shiftextra'),
        ),
        migrations.AddField(
            model_name='shift',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workhours.week', verbose_name='Неделя'),
        ),
        migrations.AddConstraint(
            model_name='week',
            constraint=models.UniqueConstraint(fields=('team', 'starting_date'), name='week_unique_team_starting_date'),
        ),
        migrations.AddConstraint(
            model_name='shiftextra',
            constraint=models.UniqueConstraint(fields=('shift', 'extra'), name='shiftextra_unique_shift_extra'),
        ),
        migrations.AddConstraint(
            model_name='shift',
            constraint=models.UniqueConstraint(fields=('week', 'employee', 'date'), name='shift_unique_date_employee_date'),
        ),
    ]
