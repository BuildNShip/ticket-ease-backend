from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class CustomResponse:
    def __init__(self, message={}, general_message=[], response={}):
        if not isinstance(general_message, list):
            general_message = [general_message]

        self.message = {'general': general_message}
        self.message.update(message)
        self.response = response

    def get_success_response(self):
        return Response(
            data={
                "hasError": False,
                "statusCode": 200,
                "message": self.message,
                "response": self.response
            }, status=status.HTTP_200_OK)

    def get_failure_response(self, status_code=400, http_status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            data={
                "hasError": True,
                "statusCode": status_code,
                "message": self.message,
                "response": self.response
            }, status=http_status_code)


def get_current_utc_time():
    return timezone.now()


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def filter_params(params):
    for key, value in params.items():
        if value is None or value == "null" or value == "None" or value == "NULL":
            params[key] = None
        elif value.lower() in ["true", "false"]:
            bool_check = {'true': True, 'false': False}
            params[key] = bool_check.get(value.lower())
        elif value.isdigit():
            params[key] = int(value)
        elif is_float(value):
            params[key] = float(value)
    return params
