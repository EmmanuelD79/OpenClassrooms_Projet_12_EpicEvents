# Generated by Django 4.1.2 on 2022-10-24 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_clientstatus_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.PROTECT, to='clients.clientstatus', verbose_name='Status du Client'),
        ),
    ]