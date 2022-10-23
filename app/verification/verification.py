from users.models import User


class EmailVerificationToken:
    @classmethod
    def generate_token(cls, user: User) -> str:
        """
        TODO: generate a token such that it will give you id of the user
        """
        return ""

    @classmethod
    def decode_token(cls, token: str) -> User:

        """
        TODO: decode the token generated by the generated_token and return user
        """
        pass


class OTPVerificationToken:
    @classmethod
    def generate_token(cls, user: User) -> int:
        """
        OTP token generation
        """
        pass

    @classmethod
    def decode_token(cls, user: User, otp: int) -> bool:

        """
        TODO:   decode the token
        TODO:   check if post otp is match with the redis database otp
        TODO:   if match return True else False
        """
        pass
