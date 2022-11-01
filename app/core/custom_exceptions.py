import json
from typing import Dict, List

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class Traces:
    def __init__(self, exception: Exception) -> None:
        self.exception = exception
        self.traces = self.get_exception_traceback()

    def get_exception_traceback(self) -> List[Dict]:
        traceback = self.exception.__traceback__
        traces = []
        while traceback is not None:
            traces.append(
                {
                    "filename": traceback.tb_frame.f_code.co_filename,
                    "name": traceback.tb_frame.f_code.co_name,
                    "line_no": traceback.tb_lineno,
                }
            )
            traceback = traceback.tb_next
        return traces

    @property
    def traces_to_str(self) -> str:
        pre_str_traces = [
            json.dumps(trace, indent=4, separators=(",", ":")) for trace in self.traces
        ]
        str_traces = "\n".join(pre_str_traces)
        return f"[\n{str_traces}\n]"


class FieldDoesNotExist(APIException):
    def __init__(self, instance, field_name, message="Field does not exists") -> None:
        self.instance = instance
        self.field_name - field_name
        self.message = message
        super().__init__(self, message)

    def __str__(self) -> str:
        fields = " ".join([f"'{key}'" for key in self.instance.__dict__.keys()])
        return f"{self.__class__} -> {self.field_name} -> doest not exist in {self.instance.__class__}:[ {fields} ]"


class FormatException(APIException):
    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(self, self.message)

    def __str__(self) -> str:
        return f"{self.__class__} -> {self.message}"


class InvalidTokenType(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("Invalid Token Type")
    default_code = "invalid token type"
