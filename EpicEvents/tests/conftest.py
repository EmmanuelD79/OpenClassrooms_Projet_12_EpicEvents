import pytest
from authentication.models import Employee
from clients.models import ClientStatus, Client
from contracts.models import Contract
from events.models import EventStatus, Event
from utils.utils import InitDb
from rest_framework.test import APITestCase
from utils.data import EMPLOYEES, CLIENTS, ADMIN_USER, EVENTS_STATUS, NEW_CONTRACT


@pytest.fixture
def employee_data():
    employee = {
        'first_name': "Pierre",
        'last_name': "Jean",
        'email': "pierre.jean@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'password': "S3cr3tW0rd",
    }
    return employee


@pytest.fixture
def employee_data_2():
    employee = {
        'first_name': "Paul",
        'last_name': "Jacques",
        'email': "paul.jacques@gmail.com",
        'phone': "0506070809",
        'mobile': "0605060708",
        'password': "S3cr3tW0rd",
    }
    return employee


@pytest.fixture
def employees(employee_data_2, employee_data):
    return [employee_data, employee_data_2]


@pytest.fixture
def employee_expected_value(employee_data):
    return f"{employee_data['first_name']} {employee_data['last_name']} | {employee_data['email']}"


@pytest.fixture
def client_data():
    client = {
        'first_name': "Bill",
        'last_name': "Malone",
        'email': "bill.Malone@gmail.com",
        'phone': "0102030405",
        'mobile': "0601020304",
        'company_name': "Test Corporation",
    }
    return client


@pytest.fixture
def client_expected_value(client_data):
    return f"{client_data['first_name']} {client_data['last_name']} | {client_data['email']} | {client_data['company_name']}"


@pytest.fixture
def status_data():
    status = {'status': "Prospect"}
    return status


@pytest.fixture
def get_employee_contact(employee_data):
    return Employee.objects.create_user(**employee_data)


@pytest.fixture
def get_client_status(status_data):
    return ClientStatus.objects.create(**status_data)


@pytest.fixture
def get_contract(get_employee_contact, get_client_status, client_data):
    contract = Contract.objects.create(
                payment_due=NEW_CONTRACT['payment_due'],
                amount_float=NEW_CONTRACT['amount_float'],
                client_id=Client.objects.create(
                        **client_data,
                        sales_contact_id=get_employee_contact,
                        status=get_client_status),
                status=False,
                name=NEW_CONTRACT['name']
            )
    return contract


@pytest.fixture
def get_status_event():
    event_status = EventStatus.objects.create(status=EVENTS_STATUS[0])
    return event_status


class ViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        InitDb.run()
        InitDb.create_admin_user()

        cls.sales_contact = Employee.objects.get(email=EMPLOYEES[0]['email'])
        cls.support_contact = Employee.objects.get(email=EMPLOYEES[1]['email'])
        cls.client_test = Client.objects.get(email=CLIENTS[0]['email'])
        cls.admin_user = Employee.objects.get(email=ADMIN_USER['email'])
        cls.contract = Contract.objects.all().first()
        cls.event = Event.objects.all().first()

    def login_user(self, user_email):
        user = Employee.objects.get(email=user_email)
        self.client.force_login(user=user)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def format_date(self, value):
        return value.strftime("%Y-%m-%d")
