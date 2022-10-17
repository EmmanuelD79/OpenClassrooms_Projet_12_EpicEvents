from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, GroupManager
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
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
        
        extra_fields.setdefault('group_name', group)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Group(models.Model):
    
    name = models.CharField("Service", max_length=30, primary_key=True)
    permissions = models.ManyToManyField(Permission, verbose_name="autorisation", related_name="authorization")

    objects = GroupManager()

    class Meta:
        verbose_name="Groupe"
        verbose_name_plural = "Groupes"
    
    def __str__(self):
        return f"{self.name}"

class Employee(AbstractBaseUser, PermissionsMixin):
    
    first_name = models.CharField("Prénom", max_length=25,blank=False)
    last_name = models.CharField("Nom", max_length=25, blank=False)
    email = models.EmailField("Email", max_length=50, blank=False, unique=True)
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
    date_created = models.DateTimeField("Crée le", auto_now_add=True)
    date_updated = models.DateTimeField("Mise à jour le", auto_now=True)
    group_name = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Groupe")
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    
    class Meta:
        verbose_name="Salariée"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email} | {self.group_name}"
    