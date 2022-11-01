from functools import wraps
from typing import Union

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.transaction import atomic
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.custom_exceptions import Traces


def get_exception_response(exe: Union[Exception, None]):
    pass


def exception_grabber(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            with atomic():
                return func(*args, **kwargs)
        except ObjectDoesNotExist as does_not_exist_exception:
            # traces = get_exception_traceback(does_not_exist_exception)
            print(does_not_exist_exception)
            # print(f"traceback:{traces}")
            return Response(
                {
                    "error": f"{does_not_exist_exception.__class__.__name__} - > {does_not_exist_exception}"
                }
            )

        except MultipleObjectsReturned as mor:
            print("MultipleObjectsReturned", mor)
            return Response({"error": f"{mor.__class__.__name__} - > {mor}"})

        except ValidationError as validation_error:
            print("ValidationError", validation_error)
            response = exception_handler(validation_error, "")
            return response

        except AuthenticationFailed as auth_exc:
            traces = Traces(auth_exc)
            print("AuthenticationFailed", traces.traces_to_str)
            return Response({"detail": f"{auth_exc}"})

        except Exception as exc:
            """
            TODO: handle for different exceptions such as
            Format Exception
            Does not Exist

            """
            traces = Traces(exc)
            print("trace backs ", traces.traces_to_str)
            return Response({"error": f"{exc.__class__.__name__} - > {exc}"})

    return wrapper
