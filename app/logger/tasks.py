import os
from datetime import datetime
from typing import Dict, List, Optional

from celery import shared_task
from core.celery import app
from core.custom_exceptions import Traces
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


@app.task
def create_directory(path: str) -> None:
    base_path = os.path.basename(path)
    os.mkdir(base_path)
    return


@app.task
def create_file(path: str) -> None:
    try:
        with open(path) as file:
            pass
    except OSError as e:
        if getattr(settings, "DEBUG"):
            print(e)
        create_directory(path)
        create_file(path)


@app.task
def write_log(file_name: str, exception: Exception, level: str) -> str:
    from django.conf import settings

    path = f"{settings.BASE_DIR}/logs/django/{file_name}.log"
    if not os.path.exists(path):
        create_file(path)
    with open(path, "a+") as log:
        for count, lines in enumerate(log):
            pass
        tracebacks = Traces(exception)
        log.writelines(
            f"{count+1} [ {datetime.now()} ] % {level.upper()} % -> {exception.__class__} : {exception} % traceback % {tracebacks.traces_to_str}"
        )

    if (
        level == "ERROR"
        or level == "error"
        or level == "CRITICAL"
        or level == "critical"
    ):
        message = f"The error has occurred. Please check the log file : {file_name}. line: {count +1} "
        send_email(subject="Error occurred", message=message, error_level=level)
    return "log updated"


@shared_task
def send_email(
    subject: str,
    message: str,
    receiver: Optional[List[str]] = None,
    error_level: Optional[str] = None,
    obj: Optional[Dict] = None,
    template_name: Optional[str] = None,
    use_template: Optional[bool] = False,
) -> str:
    """
    This function requires to have the folder email in templates folder of the root directory
    template_name should be similar for both text and email as given in default, works for custom too

    """

    if receiver is None:
        receiver = settings.ADMINS
        if error_level is not None:
            subject = f"{error_level.upper()} " + subject
    sender = settings.DEFAULT_FROM_EMAIL
    if use_template:
        context = {message, obj}
        if template_name is None:
            text_ = get_template("emails/email.txt").render(context)
            html_ = get_template("emails/email.html").render(context)
        else:
            text_ = get_template(f"emails/{template_name}.txt").render(context)
            html_ = get_template(f"emails/{template_name}.html").render(context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_,
            to=receiver,
            from_email=sender,
        )
        email.attach_alternative(html_, "text/html")
    else:
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            to=receiver,
            from_email=sender,
        )
    try:
        email.send(fail_silently=False)
        return f"{email.__dict__} is sended successfully"
    except Exception as e:
        if getattr(settings, "DEBUG"):
            print(e)
        write_log.delay(file_name="email", exception=e, level="INFO")
