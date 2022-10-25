# Generated by Django 4.1.2 on 2022-10-25 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='events.eventstatus', verbose_name="Etat d'avancement"),
        ),
    ]
