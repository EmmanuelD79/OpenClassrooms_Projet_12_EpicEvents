import pytest
from events.models import Event, EventStatus
from authentication.models import Employee, Group
from clients.models import Client, ClientStatus
from datetime import date


@pytest.mark.django_db 
def test_event_status_model():
    statut = EventStatus.objects.create(status="En préparation")
    assert str(statut) == "En préparation"


@pytest.mark.django_db
class TestClient:
    pytestmark = pytest.mark.django_db

    def test_should_create_event_model(self):
        
        statut = EventStatus.objects.create(status="En préparation")
        
        sales_contact = Employee.objects.create_user(
            first_name="test",
            last_name="test",
            email="test@gmail.com",
            group_name=Group.objects.create(name="Support"))
        
        client_id = Client.objects.create(
            first_name = "Pierre",
            last_name = "Jean",
            email = "pierre.jean@gmail.com",
            phone = "0102030405",
            mobile = "0601020304",
            company_name = "Test Corporation",
            sales_contact_id = sales_contact,
            status = ClientStatus.objects.create(status="Client"))
    
        event = Event.objects.create(
            event_date = date.today(),
            attendees = 150,
            support_contact_id = sales_contact,
            event_status = statut,
            client_id = client_id,
        )
        
        expected_value = f"Test Corporation | test@gmail.com | En préparation | {date.today()} | 150"
        assert str(event) == expected_value
        assert Event.objects.count() == 1
    