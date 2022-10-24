from django.urls import reverse_lazy, reverse
from tests.conftest import ViewTest
from clients.models import Client
from authentication.models import Employee
from utils.utils import InitDb
from utils.data import EMPLOYEES, NEW_CLIENT, ADMIN_USER
from parametrize import parametrize


class ClientTest(ViewTest):

    def get_client_list_data(self, clients):
        return [
            {
                'id': client_test.id,
                'first_name': client_test.first_name,
                'last_name': client_test.last_name,
                'email': client_test.email,
                'phone': client_test.phone,
                'mobile': client_test.mobile,
                'company_name': client_test.company_name,
                'status': client_test.status.pk,
                'sales_contact_id': client_test.sales_contact_id.id
            } for client_test in clients
        ]
    
    def get_client_detail_data(self, client, status_code):
        
        if status_code == 200:
            detail_data = {
                'id': client.id,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'email': client.email,
                'phone': client.phone,
                'mobile': client.mobile,
                'company_name': client.company_name,
                'status': client.status.status,
                'sales_contact_id': client.sales_contact_id.id
            }
        elif status_code == 403:
            detail_data = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
        
        return detail_data
        
        
class ClientViewsetTests(ClientTest):
    
    url = reverse_lazy('client-list')
    
    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 200),
                     (EMPLOYEES[0]['email'], 200),
                     (EMPLOYEES[1]['email'], 200)   
                 ])
    def test_client_list(self, user_email, status_code):
        self.login_user(user_email)
        user = Employee.objects.get(email=user_email)
        if user.is_superuser:
            self.clients_test = Client.objects.all()
        else:
            self.clients_test = Client.objects.filter(sales_contact_id=user).order_by('id') | Client.objects.filter(contract__event__support_contact_id=user).order_by('id')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_code)
        expected = self.get_client_list_data(self.clients_test)
        self.assertEqual(response.json()['results'], expected)

    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 201),
                     (EMPLOYEES[0]['email'], 201),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_client_create(self, user_email, status_code):
        self.login_user(user_email)
        client_count = Client.objects.count()
        response = self.client.post(self.url, data=NEW_CLIENT)
        self.assertEqual(response.status_code, status_code)
        if status_code == 201:
            self.assertEqual(Client.objects.count(), client_count+1)
        elif status_code == 403:
            self.assertEqual(Client.objects.count(), client_count)
        InitDb.refresh_db()
    
    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 200),
                     (EMPLOYEES[0]['email'], 200),
                     (EMPLOYEES[1]['email'], 200)   
                 ])
    def test_client_detail(self, user_email, status_code):
        self.login_user(user_email)
        # Nous utilisons l'url de détail
        url_detail = reverse('client-detail',kwargs={'pk': self.client_test.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, status_code)
        excepted = self.get_client_detail_data(self.client_test, status_code)
        self.assertEqual(excepted, response.json())
        InitDb.refresh_db()
        
    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 200),
                     (EMPLOYEES[0]['email'], 200),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_update(self, user_email, status_code):
        self.login_user(user_email)
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
        if status_code == 200:
            excepted = {'id': self.client_test.pk,}
            excepted.update(data)
        elif status_code == 403:
            excepted = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
        response = self.client.put(url_detail, data=data)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(excepted, response.json())
        InitDb.refresh_db()

    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 204),
                     (EMPLOYEES[0]['email'], 403),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_delete(self, user_email, status_code):
        self.login_user(ADMIN_USER['email'])
        self.client.post(self.url, data=NEW_CLIENT)
        new_client = Client.objects.get(email=NEW_CLIENT['email'])
        self.login_user(user_email)
        response = self.client.delete(reverse('client-detail', kwargs={'pk': new_client.pk}))
        self.assertEqual(response.status_code, status_code)
        InitDb.refresh_db()