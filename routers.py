from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, auth
from .dependencies import get_current_user
from .db import get_session
from .utils import import_from_path, hash_fingerprint


router = APIRouter()

UserModel = import_from_path(auth.Config.USER_MODEL)


@router.post("/login", response_model=schemas.Token)
async def login(
    data: schemas.Login,
    db: AsyncSession = Depends(get_session)
):
    user = await auth.authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
        
    fp_hash = hash_fingerprint(data.fingerprint)

    access_token = await auth.create_access_token({"sub": user.id})
    refresh_token = await auth.create_refresh_token(user.id, db, data.device_name, fp_hash)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=schemas.Token)
async def refresh(
    data: schemas.TokenRefresh,
    db: AsyncSession = Depends(get_session)
):
    payload = await auth.verify_token(data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    q = await db.execute(select(RefreshToken).where(RefreshToken.token == data.refresh_token))
    refresh_token = q.scalar_one_or_none()
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    fp_hash = hash_fingerprint(data.fingerprint)
    if refresh_token.fingerprint_hash != fp_hash:
        raise HTTPException(status_code=401, detail="Device mismatch")
    
    new_access = await auth.create_access_token({"sub": payload["sub"]})
    new_refresh = await auth.rotate_refresh_token(
        data.refresh_token, payload["sub"], db, refresh_token.device_name, refresh_token.fingerprint_hash
    )
    return {"access_token": new_access, "refresh_token": new_refresh}


@router.post("/logout")
async def logout(
    data: schemas.TokenRefresh,
    db: AsyncSession = Depends(get_session)
):
    await auth.blacklist_refresh_token(data.refresh_token, db)
    return {"detail": "Logged out"}


@router.post("/logout_all")
async def logout_all(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    sessions = await auth.get_active_sessions(user.id, db)
    for s in sessions:
        await auth.blacklist_refresh_token(s.token, db)
    return {"detail": "All sessions logged out"}


@router.get("/active_sessions", response_model=list[schemas.DeviceSession])
async def active_sessions(
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    tokens = await auth.get_active_sessions(user.id, db)
    return [{
        "refresh_token": t.token,
        "device_name": t.device_name,
        "created_at": t.created_at.isoformat()
    } for t in tokens]


@router.post("/revoke_other_session")
async def revoke_other_session(
    data: schemas.TokenRefresh,
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    await auth.revoke_other_sessions(user.id, data.refresh_token, db)
    return {"detail": "Other sessions revoked"}