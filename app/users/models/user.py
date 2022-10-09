from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self, email, mobile, password=None, is_staff=False, is_active=False
    ):
        if not email:
            raise ValueError(_("Email is Required."))
        if not mobile:
            raise ValueError(_("Phone number is Required."))

        user = self.model(
            email=self.normalize_email(email),
            mobile=self.mobile,
            is_active=is_active,
            is_admin=is_staff,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, mobile, password=None, is_staff=True, is_active=True
    ):
        user = self.create_user(
            email,
            mobile,
            password=password,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    mobile_regex = RegexValidator(
        regex=r"^\+[1-9]{1,3}[789][0-9]{9}$",
        message=_(
            "phone number should at least contain 10 digit with country code. eg: +9776568456545 "
        ),
    )

    email = models.EmailField(_("Email Address"), unique=True, null=False, blank=False)
    mobile = models.CharField(
        _("Phone number"),
        max_length=14,
        validators=[mobile_regex],
        unique=True,
        editable=False,
        null=False,
        blank=False,
        help_text="Please use following format: <Country code><mobile-number>",
    )

    is_active = models.BooleanField(_("Active"), default=False)
    is_admin = models.BooleanField(_("Staff Member"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    class Meta:
        indexes = [models.Index(fields=["email", "mobile"])]

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
