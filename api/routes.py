from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from crud import create_secret, delete_secret, check_secret_and_make_logs
from db import get_session
from dependencies import secret_by_secret_key
from models import Secret
from schemas import (
    SecretCreateRequest,
    SecretCreateResponse,
    SecretReadResponse,
    SecretDeleteResponse,
)

router = APIRouter(prefix="/api")


@router.post("/secret", response_model=SecretCreateResponse)
async def create_new_secret(
    secret_in: SecretCreateRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    key = await create_secret(
        secret_data=secret_in,
        request=request,
        session=session,
    )
    return {"secret_key": key}


@router.get("/secret/{secret_key}", response_model=SecretReadResponse)
async def get_secret_by_secret_key(
    request: Request,
    secret: Secret = Depends(secret_by_secret_key),
    session: AsyncSession = Depends(get_session),
):
    decrypt_secret = await check_secret_and_make_logs(
        secret=secret,
        request=request,
        session=session,
    )
    return {"secret": decrypt_secret}


@router.delete("/secret/{secret_key}", response_model=SecretDeleteResponse)
async def delete_secret_by_secret_key(
    request: Request,
    secret: Secret = Depends(secret_by_secret_key),
    session: AsyncSession = Depends(get_session),
):
    status = await delete_secret(
        secret=secret,
        request=request,
        session=session,
    )
    return {"status": status}
