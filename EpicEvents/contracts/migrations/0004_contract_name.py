# Generated by Django 4.1.2 on 2022-10-18 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0003_remove_contract_sales_contact_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='name',
            field=models.CharField(default=0, max_length=100, verbose_name="Nom de l'événement"),
            preserve_default=False,
        ),
    ]
