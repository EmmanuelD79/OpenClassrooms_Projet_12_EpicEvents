from django.db import models
from authentication.models import Employee, PhoneInfo, DateTimeInfo


class ClientStatus(models.Model):
    status = models.CharField(max_length=30, verbose_name='status', primary_key=True)

    class Meta:
        verbose_name_plural = "Client Status"

    def __str__(self):
        return f"{self.status}"


class Client(PhoneInfo, DateTimeInfo):
    first_name = models.CharField("Prénom", max_length=25, blank=False)
    last_name = models.CharField("Nom", max_length=25, blank=False)
    email = models.EmailField("Email", max_length=50, blank=False, unique=True)

    company_name = models.CharField("Société", max_length=100, blank=False)
    sales_contact_id = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Commercial")
    status = models.ForeignKey(ClientStatus, max_length=25, blank=False, verbose_name='Status du Client', on_delete=models.PROTECT)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.email} | {self.company_name}"
