from pydantic import BaseModel
from users.models import User


class VerificationModel(BaseModel):
    token: str
    is_verified: bool = False
    user: User


class OTPModel(BaseModel):
    otp: int
    user: User
