from django.urls import reverse_lazy, reverse
from tests.conftest import ViewTest
from clients.models import Client
from contracts.models import Contract
from authentication.models import Employee
from datetime import date
from authentication.utils import InitDb
from tests.datas import EMPLOYEES, ADMIN_USER, NEW_CONTRACT, CLIENTS
from parametrize import parametrize
import json

class ContractTest(ViewTest):

    def format_date(self, value):
        return value.strftime("%Y-%m-%d")
    
    def get_contract_list_data(self, contracts, status_code):
        if status_code == 200:
            list_data = [{
                'id': contract.pk,
                'client_id': contract.client_id.id,
                'status': contract.status,
                'payment_due': self.format_date(contract.payment_due),
                'amount_float': contract.amount_float,
                'name': contract.name
            } for contract in contracts]
        elif status_code == 403:
            list_data = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
    
        return list_data
    
    def get_contract_detail_data(self, contract, status_code):
        if status_code == 200:
            detail_data= {
                'id': contract.pk,
                'client_id': contract.client_id.id,
                'status': contract.status,
                'payment_due': self.format_date(contract.payment_due),
                'amount_float': contract.amount_float,
                'name': contract.name
                }
        elif status_code == 403:
            detail_data = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
        return detail_data


class ContractViewsetTests(ContractTest):   
    url = reverse_lazy('contract-list')
    
    
    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 200),
                     (EMPLOYEES[0]['email'], 200),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_contract_list(self, user_email, status_code):
        self.login_user(user_email)
        user = Employee.objects.get(email=user_email)
        if user.is_superuser:
            self.contracts = Contract.objects.all()
        else:
            self.contracts = Contract.objects.filter(client_id__sales_contact_id=user)| Contract.objects.filter(event__support_contact_id=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_code)
        expected = self.get_contract_list_data(self.contracts, status_code)
        if status_code == 200:
            self.assertEqual(response.json()['results'], expected)
        elif status_code == 403:
            self.assertEqual(response.json(), expected)
        InitDb.refresh_db()

    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 201),
                     (EMPLOYEES[0]['email'], 201),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_contract_create(self, user_email, status_code):
        self.login_user(user_email)
        client_id = Client.objects.get(email=CLIENTS[0]['email'])
        NEW_CONTRACT['client_id']= client_id.pk
        contract_count = Contract.objects.count()
        response = self.client.post(self.url, data=NEW_CONTRACT)
        self.assertEqual(response.status_code, status_code)
        if status_code == 201:
            self.assertEqual(Contract.objects.count(), contract_count+1)
        elif status_code == 403:
            self.assertEqual(Contract.objects.count(), contract_count)
        InitDb.refresh_db()
    
    
    @parametrize('user_email, status_code', 
                 [
                     (ADMIN_USER['email'], 200),
                     (EMPLOYEES[0]['email'], 200),
                     (EMPLOYEES[1]['email'], 403)   
                 ])
    def test_contract_detail(self, user_email, status_code):
        self.login_user(user_email)

        url_detail = reverse('contract-detail',kwargs={'pk': self.contract.pk})
        response = self.client.get(url_detail)
        
        self.assertEqual(response.status_code, status_code)
        excepted = self.get_contract_detail_data(self.contract, status_code)
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
        url_detail = reverse('contract-detail',kwargs={'pk': self.contract.pk})
        data = {
                'client_id': self.client_test.id,
                'status': True,
                'payment_due': self.format_date(date.today()),
                'amount_float': 1000.40,
                'name': 'la fête de la biere'
        }
        if status_code == 200:
            excepted = {'id': self.contract.pk,}
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
        client_id = Client.objects.get(email=CLIENTS[0]['email'])
        NEW_CONTRACT['client_id']= client_id.pk
        self.client.post(self.url, data=NEW_CONTRACT)
        new_contract = Contract.objects.get(name=NEW_CONTRACT['name'])
        self.login_user(user_email)
        response = self.client.delete(reverse('contract-detail', kwargs={'pk': new_contract.pk}))
        self.assertEqual(response.status_code, status_code)
        InitDb.refresh_db()
        
