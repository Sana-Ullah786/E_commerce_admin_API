from pydantic import BaseModel, constr


class UserSchema(BaseModel):
    """
    A Base Pydantic model for user.
    """

    username: constr(strip_whitespace=True, min_length=3, max_length=32)
    password: constr(min_length=8, max_length=16)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe123",
                "password": "John_Doe987",
            }
        }


class UserSchemaToken(BaseModel):

    """
    A Pydantic user schema that will be used to return the token.
    """

    access_token: str
