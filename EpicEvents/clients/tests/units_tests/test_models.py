import pytest
from clients.models import Client, ClientStatus
from authentication.models import Employee, Group


@pytest.mark.django_db 
def test_client_status_model():
    statut = ClientStatus.objects.create(status="Prospect")
    assert str(statut) == "Prospect"


@pytest.mark.django_db
class TestClient:
    pytestmark = pytest.mark.django_db
    
    def test_should_create_client_model(self):

        client = Client.objects.create(
                    first_name = "Pierre",
                    last_name = "Jean",
                    email = "pierre.jean@gmail.com",
                    phone = "0102030405",
                    mobile = "0601020304",
                    company_name = "Test Corporation",
                    sales_contact_id = Employee.objects.create_user(first_name="test", last_name="test", email="test@gmail.com", group_name=Group.objects.create(name="Sales")),
                    status = ClientStatus.objects.create(status="Prospect")
                )
        expected_value = "Pierre Jean | pierre.jean@gmail.com | Test Corporation"
        assert str(client) == expected_value
        assert Client.objects.count() == 1
        
    def test_verbose_name_for_status(self):
        for field in Client._meta.fields:
            if field.name ==  'status':
                assert field.verbose_name == 'client_status'