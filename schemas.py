from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class Login(BaseModel):
    username: str
    password: str


class DeviceSession(BaseModel):
    refresh_token: str
    created_at: str