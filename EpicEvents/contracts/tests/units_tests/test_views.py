from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from clients.models import Client, ClientStatus
from contracts.models import Contract
from authentication.models import Employee, Group
from datetime import date

class ContractTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sales_contact_group = Group.objects.create(name="Sales")
        cls.sales_contact = Employee.objects.create_user(
                first_name="test",
                last_name="test",
                email="test@gmail.com",
                password="S3cr3tW0rld",
                group_name = cls.sales_contact_group   
                )
        cls.client_status = ClientStatus.objects.create(status="Prospect")  
        cls.client_test = Client.objects.create(
                    first_name = "Pierre",
                    last_name = "Jean",
                    email = "pierre.jean@gmail.com",
                    phone = "0102030405",
                    mobile = "0601020304",
                    company_name = "Test Corporation",
                    sales_contact_id = cls.sales_contact ,
                    status = cls.client_status
                )
        
        cls.contract = Contract.objects.create(
                    payment_due = date.today(),
                    amount_float = 30000.40,
                    client_id = cls.client_test,
                    sales_contact_id = cls.sales_contact
                )
        
    def login_user(self):
        user = Employee.objects.get(email= self.sales_contact.email)
        self.client.force_login(user=user)
        
        
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def format_date(self, value):
        return value.strftime("%Y-%m-%d")
    
    def get_contract_list_data(self, contracts):
        return [
            {
                'id': contract.pk,
                'client_id': contract.client_id.id,
                'status': contract.status,
                'payment_due': contract.payment_due,
                'amount_float': contract.amount_float,
                'sales_contact_id': contract.sales_contact_id.id,
            } for contract in contracts
        ]
    
    def get_contract_detail_data(self, contract):
        return {
            'id': contract.pk,
            'client_id': contract.client_id.id,
            'status': contract.status,
            'payment_due': contract.payment_due,
            'amount_float': contract.amount_float,
            'sales_contact_id': contract.sales_contact_id.id,
            'date_created': self.format_datetime(contract.date_created),
            'date_updated': self.format_datetime(contract.date_updated),
        }


class ContractViewsetTests(ContractTest):   
    url = reverse_lazy('contract-list')

    def test_contract_list(self):
        self.login_user()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': contract.pk,
                'client_id': contract.client_id.id,
                'status': contract.status,
                'payment_due': self.format_date(contract.payment_due),
                'amount_float': contract.amount_float,
                'sales_contact_id': contract.sales_contact_id.id,
            } for contract in [self.contract]
        ]
        self.assertEqual(response.json(), expected)

    def test_contract_create(self):
        self.login_user()
        contract_count = Contract.objects.count()
        data = {
                'payment_due': self.format_date(date.today()),
                'amount_float': 1000.40,
                'client_id': self.client_test.id,
                'status': False
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), contract_count+1)
    
    def test_contract_detail(self):
        self.login_user()
        # Nous utilisons l'url de détail
        url_detail = reverse('contract-detail',kwargs={'pk': self.contract.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)
        excepted = {
                'id': self.contract.pk,
                'client_id': self.contract.client_id.id,
                'status': self.contract.status,
                'payment_due': self.format_date(self.contract.payment_due),
                'amount_float': self.contract.amount_float,
                'sales_contact_id': self.contract.sales_contact_id.id,
        }
        self.assertEqual(excepted, response.json())
        
    def test_update(self):
        self.login_user()
        url_detail = reverse('contract-detail',kwargs={'pk': self.contract.pk})
        data = {
                'client_id': self.client_test.id,
                'status': True,
                'payment_due': self.format_date(date.today()),
                'amount_float': 1000.40,
        }
        
        excepted = {'id': self.contract.pk,}
        excepted.update(data)
        excepted['sales_contact_id']= self.contract.sales_contact_id.id
        
        response = self.client.put(url_detail, data=data)
        self.assertEqual(excepted, response.json())
        
    def test_delete(self):
        self.login_user()
        response = self.client.delete(reverse('contract-detail', kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 204)
