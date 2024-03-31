import pytest
from apps.users.models import PatientCard


@pytest.mark.django_db
def test_card_patient_exists(card_factory):
    patient_card = card_factory.build()
    assert patient_card.patient.user.email == "test@gmail.com"
    assert patient_card.patient is not None


@pytest.mark.django_db
def test_card_model(card_factory):
    patient_card = card_factory.build()
    assert isinstance(patient_card, PatientCard)


@pytest.mark.django_db
def test_card_model_doctor_exists(card_factory):
    patient_card = card_factory.build()
    assert patient_card.doctor_owners is not None
