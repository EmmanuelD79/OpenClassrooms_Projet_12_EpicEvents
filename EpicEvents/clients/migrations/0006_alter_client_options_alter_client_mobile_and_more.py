# Generated by Django 4.1.2 on 2022-10-25 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_client_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Portable'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Téléphone'),
        ),
    ]
