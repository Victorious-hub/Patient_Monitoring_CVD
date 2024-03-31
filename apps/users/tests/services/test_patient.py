import pytest

from django.http import Http404
from apps.users.exceptions import EmailException, MobileException, PasswordLengthException
from apps.users.services import patient_create, patient_update

# @pytest.mark.django_db
# def test_patient_slug(patient_factory):
#     patient = patient_factory.create()
#     assert patient.user.slug == patient.user.email.split('@')[0]


@pytest.mark.django_db
def test_patient_create_invalid_password(patient_service_invalid_password):
    # wtf.
    user = patient_service_invalid_password
    with pytest.raises(PasswordLengthException):
        patient_create(user=user, address="some test text")


@pytest.mark.django_db
def test_patient_create_email_exists(patient_service_email_exists):
    user = patient_service_email_exists
    patient_create(user=user, address="some test text")

    with pytest.raises(EmailException):
        patient_create(user=user, address="some test text")


@pytest.mark.django_db
def test_patient_create_mobile_invalid(patient_service_mobile_exists):
    user = patient_service_mobile_exists

    with pytest.raises(MobileException):
        patient_create(user=user, address="some test text")


@pytest.mark.django_db
def test_patient_updated(patient_service_update):
    user = patient_service_update
    patient_create(user=user, address="some test text")

    with pytest.raises(Http404):
        patient_update(user=user, address="some test text", slug="e")  # check for user's slug

    assert patient_update(user=user, address="some test text", slug=user['slug'])
