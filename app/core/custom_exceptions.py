from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


def get_exception_traceback(ex: Exception) -> str:
    traceback = ex.__traceback__
    traces = ""
    while traceback is not None:
        traces += f"[\n\tfilename: {traceback.tb_frame.f_code.co_filename} \n\tname: {traceback.tb_frame.f_code.co_name} \n\tline no: {traceback.tb_lineno}\n]\n"
        traceback = traceback.tb_next
    return traces


class FieldDoesNotExist(Exception):
    def __init__(self, instance, field_name, message="Field does not exists") -> None:
        self.instance = instance
        self.field_name - field_name
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        fields = " ".join([f"'{key}'" for key in self.instance.__dict__.keys()])
        return f"{self.__class__} -> {self.field_name} -> doest not exist in {self.instance.__class__}:[ {fields} ]"


class FormatException(Exception):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(self, self.message)

    def __str__(self) -> str:
        return f"{self.__class__} -> {self.message}"


class InvalidTokenType(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("Invalid Token Type")
    default_code = "invalid token type"
