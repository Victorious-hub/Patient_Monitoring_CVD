from django.http import Http404
import pytest
from apps.users.selectors import patient_get, patient_list


@pytest.mark.django_db
def test_patient_list(patient_factory):
    patient_factory.create()
    patient = patient_list()
    assert len(patient) > 0


@pytest.mark.django_db
def test_patient_retrieve(patient_factory):
    user = patient_factory.create()
    patient = patient_get(slug=user.slug)
    assert patient

    with pytest.raises(Http404):
        patient_get(slug="unexisted patient instance")
