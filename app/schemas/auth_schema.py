from pydantic import BaseModel, EmailStr, constr

class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=6)  # type: ignore

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "password": "StrongPass123"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "password": "StrongPass123"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                "token_type": "bearer"
            }
        }
