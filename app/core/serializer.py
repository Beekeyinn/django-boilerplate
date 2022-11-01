import base64
from datetime import datetime
from uuid import uuid4

import six
from core.custom_exceptions import FormatException
from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField

from core.utils import datetime_to_str


class Base64Field(ImageField):
    """
    Accepts Base64 encoded file and converts it into file with unique name
    """

    def to_internal_value(self, data: str):
        try:
            if isinstance(data, six.string_types) and data.startswith("data:image"):
                format, img_str = data.split(";base64,")
                ext = format.split("/")[-1]
                data = ContentFile(
                    base64.b64decode(img_str),
                    name=f"{uuid4()}-{datetime_to_str(datetime.now())}.{ext}",
                )
        except Exception as e:
            raise FormatException(f"Invalid Format exception: {e}")
        return super().to_internal_value(data)
