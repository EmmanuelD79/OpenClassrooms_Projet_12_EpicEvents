import pytest

from django.urls import reverse
from django.test import Client
from authentication.models import Employee


@pytest.mark.django_db
class TestLogin:
    pytestmark = pytest.mark.django_db

    def test_login_view_with_good_user(self, employee_data):
        client = Client()
        Employee.objects.create_user(**employee_data)
        path = reverse('login')
        response = client.post(path, {'email': employee_data['email'], 'password': employee_data['password']})
        assert response.status_code == 200
        assert response.data["msg"] == "Login Success"
        assert response.data["access"] != ""
        assert response.data["refresh"] != ""

    @pytest.mark.parametrize("request_data, status_code, msg", [
                                ({'email': "pierre.jean@gmail.com"}, 400, "Credentials missing"),
                                ({'password': "S3cr3tW0rd"}, 400, "Credentials missing"),
                                ({'email': "pierre.jean@gmail.com", 'password': "S3cr3tW0rd"}, 401, "Invalid Credentials")
                            ])
    def test_login_view_with_missing_attribut_or_user_not_in_db(self, request_data, status_code, msg):
        client = Client()
        path = reverse('login')
        response = client.post(path, request_data)
        assert response.status_code == status_code
        assert response.data["msg"] == msg
