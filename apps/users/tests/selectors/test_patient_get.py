from django.http import Http404
import pytest
from apps.users.models import PatientProfile
from apps.users.selectors import DoctorSelector, PatientSelector

@pytest.mark.django_db
def test_patient_list(patient_factory):
    patient_factory.create()
    patient = PatientSelector()
    data = patient.patient_list()
    assert len(data) > 0


@pytest.mark.django_db
def test_patient_retrieve(patient_factory):
    user: PatientProfile = patient_factory.create()
    patient = PatientSelector()
    data = patient.patient_get(slug=user.slug)
    assert data

    with pytest.raises(Http404):
        patient.patient_get(slug="unexisted patient instance")
    