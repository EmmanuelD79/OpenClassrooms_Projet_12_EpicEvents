from django.urls import path
from . import views
from .admin import crm_site


urlpatterns = [
    path('login/', views.LoginView, name='login'),
]