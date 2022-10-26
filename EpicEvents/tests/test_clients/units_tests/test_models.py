import pytest
from clients.models import Client, ClientStatus


@pytest.mark.django_db
def test_client_status_model(status_data):
    statut = ClientStatus.objects.create(status=status_data['status'])
    assert str(statut) == status_data['status']


@pytest.mark.django_db
class TestClient:
    pytestmark = pytest.mark.django_db

    def test_should_create_client_model(self, client_data, client_expected_value, get_employee_contact, get_client_status):
        client = Client.objects.create(
                    **client_data,
                    sales_contact_id=get_employee_contact,
                    status=get_client_status)

        expected_value = client_expected_value
        assert expected_value == str(client)
        assert Client.objects.count() == 1

    def test_verbose_name_for_status(self):
        for field in Client._meta.fields:
            if field.name == 'status':
                assert field.verbose_name == 'Status du Client'
