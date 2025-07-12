from pydantic import BaseModel
from typing import Dict


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str
    fingerprint: Dict[str, str]


class Login(BaseModel):
    username: str
    password: str
    fingerprint: Dict[str, str]
    device_name: str


class DeviceSession(BaseModel):
    refresh_token: str
    device_name: str
    created_at: str