import pytest
from clients.models import Client, ClientStatus
from contracts.models import Contract
from authentication.models import Employee, Group
from datetime import date

@pytest.mark.django_db
class TestClient:
    pytestmark = pytest.mark.django_db
    
    def test_should_create_contract_model(self):
        
        sales_contact = Employee.objects.create_user(
                    first_name="test",
                    last_name="test",
                    email="test@gmail.com",
                    group_name=Group.objects.create(name="Sales"))

        contract = Contract.objects.create(
                    payment_due = date.today(),
                    amount_float = 30000.40,
                    client_id = Client.objects.create(
                                first_name = "Pierre",
                                last_name = "Jean",
                                email = "pierre.jean@gmail.com",
                                phone = "0102030405",
                                mobile = "0601020304",
                                company_name = "Test Corporation",
                                sales_contact_id = sales_contact,
                                status = ClientStatus.objects.create(status="Prospect")),
                    sales_contact_id = sales_contact,
                    status = False
                )
        expected_value = "Test Corporation | test@gmail.com | False | 30000.4"
        assert str(contract) == expected_value
        assert Contract.objects.count() == 1
        
    
    @pytest.mark.parametrize("name_field, verbose",[
    ('client_id','client_id' ),
    ('sales_contact_id',  'sale_contact_id'),
    ])
    def test_verbose_name(self, name_field, verbose):
        for field in Contract._meta.fields:
            if field.name ==  name_field:
                assert field.verbose_name == verbose
                