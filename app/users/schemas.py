from .models import User
from pydantic import BaseModel, EmailStr, SecretStr, field_validator

class UserSignUpSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr

    @field_validator("email")
    def email_available(cls, v, values, **kwargs):
        q = User.objects.filter(email=v)
        if q.count() != 0:
            raise ValueError('Email is not available!')
        return v
    
    @field_validator("password_confirm")
    def match_passwords(cls, v, values, **kwargs):
        password = values.get("password")
        password_confirm = v
        if password != password_confirm:
            raise ValueError('Passwords do not match')
        return v

