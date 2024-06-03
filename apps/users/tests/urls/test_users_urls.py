import pdb
import pytest

from django.urls import reverse

from apps.users.models import PatientProfile
from apps.users.services import RegistrationService

@pytest.mark.django_db
def test_about_api(client):
   url = reverse('about')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_doctor_list_api(client):
   url = reverse('doctors')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_patient_list_api(client):
   url = reverse('patients')
   response = client.get(url)
   assert response.status_code == 401

@pytest.mark.django_db
def test_patient_detail_api(client):
   url = reverse('patient_detail', kwargs={'slug': 'k1'})
   response = client.get(url)
   assert response.status_code == 401

@pytest.mark.django_db
def test_patient_detail_api(client):
   url = reverse('patient_detail', kwargs={'slug': 'k1'})
   response = client.get(url)
   assert response.status_code == 401

@pytest.mark.django_db
def test_patient_detail_api(client):
   url = reverse('doctor_detail', kwargs={'slug': 'v'})
   response = client.get(url)
   assert response.status_code == 401

@pytest.mark.django_db
def test_patient_doctors_list_api(client):
   url = reverse('patient_doctors', kwargs={'slug': 'k1'})
   response = client.get(url)
   assert response.status_code == 401

@pytest.mark.django_db
def test_doctor_patients_list_api(client):
   url = reverse('doctor_patients', kwargs={'slug': 'v'})
   response = client.get(url)
   assert response.status_code == 401
   
