from django.db import models
from clients.models import Client
from authentication.models import Employee



class Contract(models.Model):
    
    date_created = models.DateTimeField("Crée le", auto_now_add=True)
    date_updated = models.DateTimeField("Mise à jour le", auto_now=True)
    payment_due = models.DateField("Date de réglement", editable=True, blank=True)
    amount_float = models.FloatField("Montant", default=0)
    client_id = models.ForeignKey(Client, max_length=25,blank=False, verbose_name='client_id', on_delete=models.CASCADE)    
    sales_contact_id = models.ForeignKey(Employee, max_length=25,blank=False, verbose_name='sale_contact_id', on_delete=models.PROTECT)    
    status = models.BooleanField("Validé", default=False)
    
    def __str__(self):
        return f"{self.client_id.company_name} | {self.sales_contact_id.email} | {self.status} | {self.amount_float}"
