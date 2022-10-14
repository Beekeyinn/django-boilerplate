import os

from app.core.custom_exceptions import FieldDoesNotExist


def remove_file(path):
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(e)


def check_and_remove_file(instance, field_name):
    klass = instance.__class__
    try:
        old_instance = klass.objects.get(id=instance.id)
        if not hasattr(instance, field_name):
            raise FieldDoesNotExist(instance, field_name)
        if getattr(old_instance, field_name) != getattr(instance, field_name):
            path = getattr(old_instance, field_name).path
            remove_file(path)
    except FieldDoesNotExist as file_exception:
        print(file_exception)
    except Exception as e:
        print(e)
