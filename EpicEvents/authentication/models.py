from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator


class DateTimeInfo(models.Model):
    date_created = models.DateTimeField("Crée le", auto_now_add=True)
    date_updated = models.DateTimeField("Mise à jour le", auto_now=True)

    class Meta:
        abstract = True


class PhoneInfo(models.Model):
    phone = models.CharField(
        "Téléphone",
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )
    mobile = models.CharField(
        "Portable",
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        group = None
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        if 'group' in extra_fields.keys():
            group = extra_fields.get('group')
            extra_fields.pop('group')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if group is not None:
            group.user_set.add(user.id)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        try:
            group = Group.objects.get(name='Management')
        except:
            group = Group.objects.create(name='Management')
            group.save()
            all_permission = Permission.objects.all()
            group.permissions.set(all_permission)
        
        extra_fields.setdefault('group', group)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Employee(AbstractUser, PermissionsMixin, DateTimeInfo, PhoneInfo):
    
    email = models.EmailField("Email", max_length=50, blank=False, unique=True)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    
    class Meta:
        verbose_name="Salariée"

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email}"
    