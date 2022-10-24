from django.urls import reverse_lazy, reverse
from contracts.models import Contract
from events.models import Event
from authentication.models import Employee
from datetime import date
from tests.conftest import ViewTest
from utils.data import EMPLOYEES, ADMIN_USER, NEW_EVENT, CONTRACTS
from parametrize import parametrize
from utils.utils import InitDb

class EventTest(ViewTest):
    
    def get_event_list_data(self, events, status_code):
        
        if status_code == 200 :
            list_data = [
                        {
                            'contract_id': event.contract_id.id,
                            'event_status': event.event_status.status,
                            'event_date': self.format_date(event.event_date),
                            'attendees': event.attendees,
                            'notes': event.notes,
                            'support_contact_id': event.support_contact_id.id,
                        } for event in events
                    ]
        elif status_code == 403:
            list_data = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
        return list_data
    
    def get_event_detail_data(self, event, status_code):
        if status_code == 200:
            detail_data = {
                'contract_id': event.contract_id.id,
                'event_status': event.event_status.status,
                'event_date': self.format_date(event.event_date),
                'attendees': event.attendees,
                'notes': event.notes,
                'support_contact_id': event.support_contact_id.id,
            }
        elif status_code == 403:
            detail_data = {'detail': "Vous n'avez pas la permission d'effectuer cette action."}
        return detail_data


class EventViewsetTests(EventTest):   
    url = reverse_lazy('event-list')

    @parametrize('user_email, status_code', 
            [
                (ADMIN_USER['email'], 200),
                (EMPLOYEES[0]['email'], 200),
                (EMPLOYEES[1]['email'], 200)   
            ])
    def test_event_list(self, user_email, status_code):
        self.login_user(user_email)
        user = Employee.objects.get(email=user_email)
        if user.is_superuser:
            self.events = Event.objects.all()
        else:
            self.events = Event.objects.filter(contract_id__client_id__sales_contact_id=user)| Event.objects.filter(support_contact_id=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_code)
        expected = self.get_event_list_data(self.events, status_code)
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
    def test_event_create(self, user_email, status_code):
        self.login_user(user_email)
        event_count = Event.objects.count()
        contract_id = Contract.objects.get(name=CONTRACTS[1]['name'])
        NEW_EVENT['contract_id']= contract_id.pk
        response = self.client.post(self.url, data=NEW_EVENT)
        self.assertEqual(response.status_code, status_code)
        if status_code == 201:
            self.assertEqual(Event.objects.count(), event_count+1)
        elif status_code == 403:
            self.assertEqual(Event.objects.count(), event_count)
        InitDb.refresh_db()
    
    
    @parametrize('user_email, status_code', 
        [
            (ADMIN_USER['email'], 200),
            (EMPLOYEES[0]['email'], 200),
            (EMPLOYEES[1]['email'], 200)   
        ])
    def test_event_detail(self, user_email, status_code):
        self.login_user(user_email)
        # Nous utilisons l'url de détail
        url_detail = reverse('event-detail',kwargs={'pk': self.event.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, status_code)
        excepted = self.get_event_detail_data(self.event, status_code)
        self.assertEqual(excepted, response.json())
        InitDb.refresh_db()
    
    @parametrize('user_email, status_code', 
            [
                (ADMIN_USER['email'], 200),
                (EMPLOYEES[0]['email'], 403),
                (EMPLOYEES[1]['email'], 200)   
            ])     
    def test_event_update(self, user_email, status_code):
        self.login_user(user_email)
        url_detail = reverse('event-detail',kwargs={'pk': self.event.pk})
        data = {
                'contract_id': self.event.contract_id.id,
                'event_status': self.event.event_status.status,
                'event_date': self.format_date(date.today()),
                'attendees': 500,
                'notes': "Second Test",
        }
        if status_code == 200:
            excepted = data
            excepted['support_contact_id']= self.event.support_contact_id.id
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
    def test_event_delete(self, user_email, status_code):
        self.login_user(user_email)
        response = self.client.delete(reverse('event-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, status_code)
        InitDb.refresh_db()
        
    