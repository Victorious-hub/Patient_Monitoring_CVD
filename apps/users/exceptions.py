from rest_framework.exceptions import APIException


class PatientCardExists(APIException):
    status_code = 400
    default_detail = 'Current patient already in patient card list'
    default_code = 'service_unavailable'


class DoctorNotFound(APIException):
    status_code = 400
    default_detail = 'Current doctor not found'
    default_code = 'service_unavailable'


class PatientNotFound(APIException):
    status_code = 400
    default_detail = 'Current patient not found'
    default_code = 'service_unavailable'


class PasswordLengthException(APIException):
    status_code = 400
    default_detail = 'Password length is too small. Must be at least 8 characters'
    default_code = 'service_unavailable'


class EmailException(APIException):
    status_code = 400
    default_detail = 'This email already exists'
    default_code = 'service_unavailable'


class MobileException(APIException):
    status_code = 400
    default_detail = "Phone does not match required format or already exists. Must be 10 charcaters like +1234567890"
    default_code = 'service_unavailable'


class PasswordOrEmailException(APIException):
    status_code = 400
    default_detail = 'Password or Email are incorrect'
    default_code = 'service_unavailable'
