# Generated by Django 4.1.2 on 2022-10-25 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_employee_options_remove_employee_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]