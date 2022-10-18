import pytest
from authentication.models import Employee, Group

    

@pytest.mark.django_db
class TestGroup:
    
    pytestmark = pytest.mark.django_db
    
    def test_group_model(self):
        group = Group.objects.create(name="Sales")
        assert str(group) == "Sales"

    def test_verbose_name_for_name(self):
        for field in Group._meta.fields:
            if field.name ==  'name':
                assert field.verbose_name == 'group'


@pytest.mark.django_db
class TestEmployee:
    pytestmark = pytest.mark.django_db
    
    def test_should_create_user_employee_model(self):
        group = Group.objects.create(name="Sales")
        employee = Employee.objects.create_user(
                    first_name = "Pierre",
                    last_name = "Jean",
                    email = "pierre.jean@gmail.com",
                    phone = "0102030405",
                    mobile = "0601020304",
                    password = "S3cr3tW0rd",
                )

        expected_value = "Pierre Jean | pierre.jean@gmail.com"
        assert str(employee) == expected_value
        assert employee.check_password("S3cr3tW0rd") == True
        assert employee.is_staff == True
        assert employee.is_superuser == False
        
    def test_should_create_superuser_employee_model(self):
        employee = Employee.objects.create_superuser(
                    first_name = "Pierre",
                    last_name = "Jean",
                    email = "pierre.jean@gmail.com",
                    phone = "0102030405",
                    mobile = "0601020304",
                    password = "S3cr3tW0rd",
                )

        expected_value = "Pierre Jean | pierre.jean@gmail.com"
        assert str(employee) == expected_value
        assert employee.check_password("S3cr3tW0rd") == True
        assert employee.is_staff == True
        assert employee.is_superuser == True
    
    def test_should_create_in_db_employee_model(self):
        group = Group.objects.create(name="Sales")
        employee1 = Employee.objects.create_user(
                    first_name = "Pierre",
                    last_name = "Jean",
                    email = "pierre.jean@gmail.com",
                    phone = "0102030405",
                    mobile = "0601020304",
                    password = "S3cr3tW0rd",

                )
        employee2 = Employee.objects.create_user(
                    first_name = "Paul",
                    last_name = "Jacques",
                    email = "paul.jacques@gmail.com",
                    phone = "0506070809",
                    mobile = "0605060708",
                    password = "S3cr3tW0rd",

                )

        assert Employee.objects.count() == 2
        