import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = not True

ALLOWED_HOSTS = [
    f"{os.getenv('DEPLOYMENT_URL')}",
    f"www.{os.getenv('DEPLOYMENT_URL')}",
]

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{os.getenv('DATABASE_ENGINE')}",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USERNAME"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "PORT": os.getenv("DATABASE_PORT"),
        "HOST": os.getenv("DATABASE_HOST"),
    }
}


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIR = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
