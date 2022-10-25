from django.db import models
from authentication.models import Employee
from contracts.models import Contract
from authentication.models import DateTimeInfo

class EventStatus(models.Model):
    status = models.CharField("Status", max_length=30, primary_key=True)
    
    class Meta:
        verbose_name_plural="Events Status"
    
    def __str__(self):
        return f"{self.status}"
    

class Event(DateTimeInfo):
    
    event_date = models.DateField("Date de l'évenement", editable=True, blank=True)
    attendees = models.PositiveIntegerField("Nb de personnes", default=0, blank=False)
    notes = models.TextField("Infos", blank=True)
    support_contact_id = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Chargé de l'événement")
    event_status = models.ForeignKey(EventStatus, on_delete=models.PROTECT, verbose_name="Etat")
    contract_id = models.OneToOneField(Contract, null=False, verbose_name='Contract', on_delete=models.PROTECT, primary_key=True)  
    
    class Meta:
        ordering = ('pk', )
    
    def __str__(self):
        return f"{self.contract_id.client_id.company_name} | {self.support_contact_id.email} | {self.event_status} | {self.event_date} | {self.attendees}"
