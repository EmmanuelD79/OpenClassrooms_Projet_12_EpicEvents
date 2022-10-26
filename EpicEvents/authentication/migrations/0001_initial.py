# Generated by Django 4.1.2 on 2022-10-26 19:34

import authentication.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Crée le')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour le')),
                ('phone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Téléphone')),
                ('mobile', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')], verbose_name='Portable')),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(max_length=256, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=256, verbose_name='Nom')),
                ('is_staff', models.BooleanField(default=True, verbose_name='utilisateur')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Administrateur')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Salariée',
                'ordering': ('email',),
            },
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
    ]
