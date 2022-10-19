from functools import wraps

from core.custom_exceptions import get_exception_traceback
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.transaction import atomic


def exception_grabber(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            with atomic():
                return func(*args, **kwargs)
        except ObjectDoesNotExist as does_not_exist_exception:
            traces = get_exception_traceback(does_not_exist_exception)
            print(does_not_exist_exception)
            print(f"traceback:{traces}")

        except MultipleObjectsReturned as mor:
            print(mor)

        except Exception as exc:
            """
            TODO: handle for different exceptions such as
            Format Exception
            Does not Exist

            """
            print(exc)

    return wrapper
