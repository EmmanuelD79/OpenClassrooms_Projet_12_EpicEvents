from django.db import models
from clients.models import Client




class Contract(models.Model):
    
    date_created = models.DateTimeField("Crée le", auto_now_add=True)
    date_updated = models.DateTimeField("Mise à jour le", auto_now=True)
    payment_due = models.DateField("Date de réglement", editable=True, blank=True)
    amount_float = models.FloatField("Montant", default=0)
    client_id = models.ForeignKey(Client, max_length=25,blank=False, verbose_name='Client', on_delete=models.CASCADE)      
    status = models.BooleanField("Validé", default=False)
    name = models.CharField("Nom de l'événement", max_length=100, blank=False)
    
    def __str__(self):
        return f"{self.client_id.company_name} | {self.name} | {self.status} | {self.amount_float}"
