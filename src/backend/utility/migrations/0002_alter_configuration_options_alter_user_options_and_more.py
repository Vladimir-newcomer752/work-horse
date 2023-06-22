# Generated by Django 4.0.5 on 2023-05-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configuration',
            options={'ordering': ['group', 'name'], 'verbose_name': 'Конфигурация', 'verbose_name_plural': 'Конфигурации'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='configuration',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='group',
            field=models.CharField(default='', max_length=255, verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='value',
            field=models.TextField(blank=True, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_last',
            field=models.BooleanField(choices=[(True, 'Показать имя + фамилию'), (False, 'Показать фамилию + имя')], default=True, verbose_name='Порядок следования имени и фамилии'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='login_redirect_page',
            field=models.CharField(blank=True, max_length=255, verbose_name='Перенаправление страницы после входа в систему'),
        ),
    ]