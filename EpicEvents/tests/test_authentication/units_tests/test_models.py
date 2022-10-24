import pytest
from authentication.models import Employee
from django.contrib.auth.models import Group

    

@pytest.mark.django_db
class TestGroup:
    
    pytestmark = pytest.mark.django_db
    
    def test_group_model(self):
        group = Group.objects.create(name="Sales")
        assert str(group) == "Sales"

@pytest.mark.django_db
class TestEmployee:
    pytestmark = pytest.mark.django_db
    
    def test_should_create_user_employee_model(self, employee_data, employee_expected_value):
        employee = Employee.objects.create_user(**employee_data)
        expected_value = employee_expected_value
        assert str(employee) == expected_value
        assert employee.check_password(f"{employee_data['password']}") == True
        assert employee.is_staff == True
        assert employee.is_superuser == False
        
    def test_should_create_superuser_employee_model(self, employee_data, employee_expected_value):
        employee = Employee.objects.create_superuser(**employee_data)
        expected_value = employee_expected_value
        assert str(employee) == expected_value
        assert employee.check_password(f"{employee_data['password']}") == True
        assert employee.is_staff == True
        assert employee.is_superuser == True
        assert "Management" in employee.groups.values_list('name', flat=True)
    
    def test_should_create_in_db_employee_model(self, employees):
        
        for employee in employees:
            Employee.objects.create_user(**employee)
        assert Employee.objects.count() == len(employees)
        