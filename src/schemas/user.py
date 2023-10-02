import re
from pydantic import BaseModel, EmailStr, constr, validator

class UserSchemaBase(BaseModel):
    """
    A Base Pydantic model for user.
    """

    email: EmailStr
    username: constr(strip_whitespace=True, min_length=3, max_length=32)
    first_name: constr(strip_whitespace=True, min_length=1, max_length=32)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=32)


class UserSchema(UserSchemaBase):

    """
    A Pydantic user schema which will be used to create a new user.
    """

    password: constr(min_length=8, max_length=16)

    @validator("password")
    def check_password(cls, v):
        pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&_*-]).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, one digit, one special character and must be at least 8 characters long."
            )
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@gmail.com",
                "username": "johndoe123",
                "password": "John_Doe987",
                "first_name": "John",
                "last_name": "Doe",
            }
        }
