from django.http import Http404
import pytest
from apps.users.selectors import doctor_get, doctor_list


@pytest.mark.django_db
def test_doctor_list(doctor_factory):
    doctor_factory.create()
    doctor = doctor_list()
    assert doctor


@pytest.mark.django_db
def test_doctor_retrieve(doctor_factory):
    user = doctor_factory.create()
    doctor = doctor_get(slug=user.slug)
    assert doctor

    with pytest.raises(Http404):
        doctor_get(slug="unexisted doctor instance")
