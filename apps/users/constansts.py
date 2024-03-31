from django.utils.translation import gettext_lazy as _

ROLES = (
    ('P', _('Patient')),
    ('D', _('Doctor')),
    ('H', _('Head')),
)

SPECS = (
    ('CS', _('Cardio Surgeon')),
    ('C', _('Cardiologist')),
)

BLOOD_TYPE = (
    ('Group I', _('I')),
    ('Group II', _('II')),
    ('Group III', _('III')),
    ('Group IV', _('IV'))
)

ALLERGIES = (
    ('pollen:pollen', _('P')),
    ('peanuts:peanuts', _('PN')),
    ('milk:milk', _('M'))
)

GENDER = (
    ('Male', _('M')),
    ('Female', _('F')),
    ('None', _('N'))
)

SMOKE = (
    ('Yes', _('1')),
    ('No', _('0'))
)

ALCO = (
    ('Yes', _('1')),
    ('No', _('0'))
)
