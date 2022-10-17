from django.urls import reverse
from django.urls import reverse_lazy, reverse
from rest_framework import status
from rest_framework.test import APITestCase
from clients.models import Client, ClientStatus
from authentication.models import Employee, Group


class ClientTest(APITestCase):
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
        
    def login_user(self):
        user = Employee.objects.get(email= self.sales_contact.email)
        self.client.force_login(user=user)
        
        
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def get_client_list_data(self, clients):
        return [
            {
                'id': client.id,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'email': client.email,
                'phone': client.phone,
                'mobile': client.mobile,
                'company_name': client.company_name,
                'status': client.status.status,
                'sales_contact_id': client.sales_contact_id.id
            } for client in clients
        ]
    
    def get_client_detail_data(self, client):
        return {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'phone': client.phone,
            'mobile': client.mobile,
            'company_name': client.company_name,
            'status': client.status.status,
            'sales_contact_id': client.sales_contact_id.id,
            'date_created': self.format_datetime(client.date_created),
            'date_updated': self.format_datetime(client.date_updated),
        }


class ClientViewsetTests(ClientTest):   
    url = reverse_lazy('client-list')

    def test_client_list(self):
        self.login_user()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
            'id': client.pk,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'phone': client.phone,
            'mobile': client.mobile,
            'company_name': client.company_name,
            'status': client.status.status,
            'sales_contact_id': client.sales_contact_id.pk
            } for client in [self.client_test]
        ]
        self.assertEqual(response.json(), expected)

    def test_client_create(self):
        self.login_user()
        client_count = Client.objects.count()
        data = {
            'first_name': "Tom",
            'last_name' : "Pierre",
            'email': "tom.pierre@gmail.com",
            'phone': "0102030405",
            'mobile': "0601020304",
            'company_name': "Start",
            'status': self.client_status.status
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Client.objects.count(), client_count+1)
    
    def test_client_detail(self):
        self.login_user()
        # Nous utilisons l'url de détail
        url_detail = reverse('client-detail',kwargs={'pk': self.client_test.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)
        excepted = {
            'id': self.client_test.pk,
            'first_name': self.client_test.first_name,
            'last_name': self.client_test.last_name,
            'email': self.client_test.email,
            'phone': self.client_test.phone,
            'mobile': self.client_test.mobile,
            'company_name': self.client_test.company_name,
            'status': self.client_test.status.status,
            'sales_contact_id': self.client_test.sales_contact_id.pk
        }
        self.assertEqual(excepted, response.json())
        
    def test_update(self):
        self.login_user()
        url_detail = reverse('client-detail',kwargs={'pk': self.client_test.pk})
        data = {
            'first_name': "Paul",
            'last_name': "Jacques",
            'email': "paul.jacques@gmail.com",
            'phone':  "0506070809",
            'mobile': "0605060708",
            'company_name': self.client_test.company_name,
            'status': self.client_test.status.status,
            'sales_contact_id': self.client_test.sales_contact_id.pk
        }
        
        excepted = {'id': self.client_test.pk,}
        excepted.update(data)
        
        response = self.client.put(url_detail, data=data)
        self.assertEqual(excepted, response.json())
        
    def test_delete(self):
        self.login_user()
        response = self.client.delete(reverse('client-detail', kwargs={'pk': self.client_test.pk}))
        self.assertEqual(response.status_code, 204)
