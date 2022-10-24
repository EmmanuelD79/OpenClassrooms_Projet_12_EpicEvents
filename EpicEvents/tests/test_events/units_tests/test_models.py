import pytest
from events.models import Event, EventStatus
from datetime import date
from utils.data import EVENTS_STATUS


@pytest.mark.django_db 
def test_event_status_model():
    statut = EventStatus.objects.create(status="En préparation")
    assert str(statut) == "En préparation"


@pytest.mark.django_db
class TestClient:
    pytestmark = pytest.mark.django_db

    def test_should_create_event_model(self, get_contract, get_employee_contact, get_status_event, client_data, employee_data):
        
        event = Event.objects.create(
            event_date = date.today(),
            attendees = 150,
            support_contact_id = get_employee_contact,
            event_status = get_status_event,
            contract_id = get_contract,
        )
        
        expected_value = f"{client_data['company_name']} | {employee_data['email']} | {EVENTS_STATUS[0]} | {date.today()} | 150"
        
        assert str(event) == expected_value
        assert Event.objects.count() == 1
    