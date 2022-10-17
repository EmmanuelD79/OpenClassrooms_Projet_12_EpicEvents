from django.db import models
from django.core.validators import RegexValidator
from authentication.models import Employee


class ClientStatus(models.Model):
    status = models.CharField(max_length=30, verbose_name='status', primary_key=True)
    
    class Meta:
        verbose_name_plural = "Client Status"
    
    def __str__(self):
        return f"{self.status}"
    

class Client(models.Model):
    
    first_name = models.CharField("Prénom", max_length=25,blank=False)
    last_name = models.CharField("Nom", max_length=25, blank=False)
    email = models.EmailField("Email",max_length=50, blank=False, unique=True)
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
    company_name = models.CharField("Société", max_length=100,blank=False)
    sales_contact_id = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Commercial")
    status = models.ForeignKey(ClientStatus, max_length=25,blank=False, verbose_name='client_status', on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email} | {self.company_name}"
