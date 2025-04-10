from fastapi import APIRouter, Depends, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession

from crud import create_secret, delete_secret, check_secret_and_make_logs
from db import get_session
from dependencies import secret_by_secret_key
from exceptions import (
    create_secret_responses,
    get_secret_responses,
    delete_secret_responses,
)
from models import Secret
from schemas import (
    SecretCreateRequest,
    SecretCreateResponse,
    SecretReadResponse,
    SecretDeleteResponse,
    SecretDeleteRequest,
)

router = APIRouter(prefix="/api", tags=["Secrets"])


@router.post(
    "/secret",
    response_model=SecretCreateResponse,
    responses=create_secret_responses,
)
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


@router.get(
    "/secret/{secret_key}",
    response_model=SecretReadResponse,
    responses=get_secret_responses,
)
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


@router.delete(
    "/secret/{secret_key}",
    response_model=SecretDeleteResponse,
    responses=delete_secret_responses,
)
async def delete_secret_by_secret_key(
    request: Request,
    delete_data: SecretDeleteRequest = Body(...),
    secret: Secret = Depends(secret_by_secret_key),
    session: AsyncSession = Depends(get_session),
):
    status = await delete_secret(
        secret=secret,
        delete_data=delete_data,
        request=request,
        session=session,
    )
    return {"status": status}
