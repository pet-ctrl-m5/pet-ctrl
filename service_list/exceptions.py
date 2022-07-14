from rest_framework.exceptions import APIException
from rest_framework.views import status


class ServiceDoesNotExists(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "service not found"
    default_code = "invalid_service"
