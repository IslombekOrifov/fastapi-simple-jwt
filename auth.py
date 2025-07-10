from datetime import datetime, timedelta, UTC

from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from .models import RefreshToken
from .settings import get_auth_config
from .utils import import_from_path


Config = get_auth_config()

pwd_context = CryptContext(schemes=Config.PASSWORD_SCHEMES, deprecated="auto")

UserModel = import_from_path(Config.USER_MODEL)
username_field = Config.USERNAME_FIELD
password_field = Config.PASSWORD_FIELD


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + Config.ACCESS_TOKEN_LIFETIME
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def create_refresh_token(user_id: int, db: AsyncSession):
    to_encode = {"sub": user_id}
    expire = datetime.now(UTC) + Config.REFRESH_TOKEN_LIFETIME
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

    db_token = RefreshToken(
        user_id=user_id,
        token=encoded_jwt,
        expires_at=expire,
    )
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return encoded_jwt


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None


async def blacklist_refresh_token(token: str, db: AsyncSession):
    db_token = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    db_token = db_token.scalar_one_or_none()
    if db_token:
        db_token.revoked = True
        await db.commit()


async def rotate_refresh_token(old_token: str, user_id: int, db: AsyncSession):
    if Config.ROTATE_REFRESH_TOKENS:
        await blacklist_refresh_token(old_token, db)
    return await create_refresh_token(user_id, db)


async def get_active_sessions(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .where(RefreshToken.revoked == False)
    )
    return result.scalars().all()


async def revoke_other_sessions(user_id: int, current_token: str, db: AsyncSession):
    result = await db.execute(
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id)
        .where(RefreshToken.token != current_token)
    )
    tokens = result.scalars().all()
    for t in tokens:
        t.revoked = True
    await db.commit()
    

async def authenticate_user(db, username: str, password: str):
    stmt = select(UserModel).where(getattr(UserModel, username_field) == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    user_password_hash = getattr(user, password_field)
    if not pwd_context.verify(password, user_password_hash):
        return None
    return user
