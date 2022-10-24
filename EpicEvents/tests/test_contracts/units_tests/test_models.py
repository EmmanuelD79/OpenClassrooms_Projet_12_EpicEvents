import pytest
from clients.models import Client
from contracts.models import Contract
from datetime import date

@pytest.mark.django_db
class TestClient:
    
    pytestmark = pytest.mark.django_db
    
    def test_should_create_contract_model(self, client_data, get_employee_contact, get_client_status): 
        contract = Contract.objects.create(
                    payment_due = date.today(),
                    amount_float = 30000.40,
                    client_id = Client.objects.create(
                            **client_data, 
                            sales_contact_id=get_employee_contact, 
                            status=get_client_status),
                    status = False,
                    name = "L'evenement du siecle",
                )
        expected_value = f"{client_data['company_name']} | L'evenement du siecle | False | 30000.4"
        assert str(contract) == expected_value
        assert Contract.objects.count() == 1

                