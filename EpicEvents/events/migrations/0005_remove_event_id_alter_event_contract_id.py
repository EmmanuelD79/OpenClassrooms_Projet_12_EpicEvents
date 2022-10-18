# Generated by Django 4.1.2 on 2022-10-18 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_contract_name'),
        ('events', '0004_remove_event_client_id_event_contract_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.AlterField(
            model_name='event',
            name='contract_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='contracts.contract', verbose_name='Contract'),
        ),
    ]