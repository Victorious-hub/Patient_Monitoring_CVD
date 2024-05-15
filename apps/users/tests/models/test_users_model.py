import pytest


@pytest.mark.django_db
def test_custom_user_patient_model(custom_user_patient_factory):
    user = custom_user_patient_factory.create()
    assert user.email == "test_patient@gmail.com"


@pytest.mark.django_db
def test_custom_user_doctor_model(custom_user_doctor_factory):
    user = custom_user_doctor_factory.create()
    assert user.email == "test_doctor@gmail.com"
