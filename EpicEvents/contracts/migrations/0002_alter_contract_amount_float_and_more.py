# Generated by Django 4.1.2 on 2022-10-16 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='amount_float',
            field=models.FloatField(default=0, verbose_name='Montant'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Crée le'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Mise à jour le'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateField(blank=True, verbose_name='Date de réglement'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Validé'),
        ),
    ]
