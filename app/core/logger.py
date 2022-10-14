import os
from datetime import datetime

from app.core.celery import app


def create_directory(path):
    base_path = os.path.basename(path)
    os.mkdir(base_path)
    return


def create_file(path):
    try:
        with open(path) as file:
            pass
    except OSError as e:
        create_directory(path)
        create_file(path)


@app.task
def write_log(file_name, exception, level):
    from django.conf import settings

    path = f"{settings.BASE_DIR}/logs/django/{file_name}.log"
    if not os.path.exists(path):
        create_file(path)
    with open(path, "a") as log:
        log.write(
            f"\n [ {datetime.now()} ] % {level.upper()} % -> {exception.__class__} : {exception} "
        )
    return "log updated"
