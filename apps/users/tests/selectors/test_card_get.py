import pytest

from apps.users.selectors import card_list
from apps.users.models import PatientCard


@pytest.mark.django_db
def test_book(patient_card):
    """Instances become fixtures automatically."""
    assert isinstance(patient_card, PatientCard)


@pytest.mark.django_db
def test_card_list(patient_card):
    card = card_list()
    assert card
