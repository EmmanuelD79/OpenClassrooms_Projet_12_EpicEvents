from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase
from clients.models import Client, ClientStatus
from events.models import Event, EventStatus
from authentication.models import Employee, Group
from datetime import date

class EventTest(APITestCase):
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
        
        cls.statut = EventStatus.objects.create(status="En préparation")
        
        cls.event = Event.objects.create(
                event_date = date.today(),
                attendees = 150,
                support_contact_id = cls.sales_contact,
                event_status = cls.statut,
                client_id = cls.client_test,
        )
        
    def login_user(self):
        user = Employee.objects.get(email= self.sales_contact.email)
        self.client.force_login(user=user)
        
        
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def format_date(self, value):
        return value.strftime("%Y-%m-%d")
    
    def get_event_list_data(self, events):
        return [
            {
                'id': event.pk,
                'client_id': event.client_id.id,
                'event_status': event.event_status,
                'event_date': self.format_date(event.event_date),
                'attendees': event.attendees,
                'notes': event.notes,
                'support_contact_id': event.support_contact_id.id,
            } for event in events
        ]
    
    def get_event_detail_data(self, event):
        return {
            'id': event.pk,
            'client_id': event.client_id.id,
            'event_status': event.event_status,
            'event_date': self.format_date(event.event_date),
            'attendees': event.attendees,
            'notes': event.notes,
            'support_contact_id': event.support_contact_id.id,
            'date_created': self.format_datetime(event.date_created),
            'date_updated': self.format_datetime(event.date_updated),
        }


class EventViewsetTests(EventTest):   
    url = reverse_lazy('event-list')

    def test_event_list(self):
        self.login_user()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'id': event.pk,
                'client_id': event.client_id.id,
                'event_status': event.event_status.status,
                'event_date': self.format_date(event.event_date),
                'attendees': event.attendees,
                'notes': event.notes,
                'support_contact_id': event.support_contact_id.id,
            } for event in [self.event]
        ]
        self.assertEqual(response.json(), expected)

    def test_event_create(self):
        self.login_user()
        event_count = Event.objects.count()
        data = {
                'client_id': self.event.client_id.id,
                'event_status': self.event.event_status.status,
                'event_date': date.today(),
                'attendees': 300,
                'notes': "Test",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), event_count+1)
    
    def test_event_detail(self):
        self.login_user()
        # Nous utilisons l'url de détail
        url_detail = reverse('event-detail',kwargs={'pk': self.event.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)
        excepted = {
                'id': self.event.pk,
                'client_id': self.event.client_id.id,
                'event_status': self.event.event_status.status,
                'event_date': self.format_date(self.event.event_date),
                'attendees': self.event.attendees,
                'notes': self.event.notes,
                'support_contact_id': self.event.support_contact_id.id,
        }
        self.assertEqual(excepted, response.json())
        
    def test_event_update(self):
        self.login_user()
        url_detail = reverse('event-detail',kwargs={'pk': self.event.pk})
        data = {
                'client_id': self.event.client_id.id,
                'event_status': self.event.event_status.status,
                'event_date': date.today(),
                'attendees': 500,
                'notes': "Second Test",
        }
        
        excepted = {'id': self.event.pk,}
        excepted.update(data)
        excepted['support_contact_id']= self.event.support_contact_id.id
        excepted['event_date']= self.format_date(date.today())
        
        response = self.client.put(url_detail, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(excepted, response.json())
        
    def test_event_delete(self):
        self.login_user()
        response = self.client.delete(reverse('event-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 204)
