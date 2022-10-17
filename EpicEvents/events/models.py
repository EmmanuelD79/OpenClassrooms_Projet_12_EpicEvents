from tabnanny import verbose
from django.db import models
from authentication.models import Employee
from clients.models import Client


class EventStatus(models.Model):
    status = models.CharField("Status", max_length=30, primary_key=True)
    
    class Meta:
        verbose_name_plural="Events Status"
    
    def __str__(self):
        return f"{self.status}"
    

class Event(models.Model):
    
    date_created = models.DateTimeField("Crée le", auto_now_add=True)
    date_updated = models.DateTimeField("Mise à jour le", auto_now=True)
    event_date = models.DateField("Date de l'évenement", editable=True, blank=True)
    attendees = models.IntegerField("Nb de personnes", default=0, blank=False)
    notes = models.TextField("Infos")
    support_contact_id = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Chargé de l'événement")
    event_status = models.ForeignKey(EventStatus, on_delete=models.PROTECT, verbose_name="Etat de l'évenement")
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    
    def __str__(self):
        return f"{self.client_id.company_name} | {self.support_contact_id.email} | {self.event_status} | {self.event_date} | {self.attendees}"
