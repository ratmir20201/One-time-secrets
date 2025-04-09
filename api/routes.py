from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from crud import create_secret, get_secret
from db import get_session
from schemas import SecretCreateRequest, SecretCreateResponse

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


@router.post("/secret/{secret_key}", response_model=SecretCreateResponse)
async def create_new_secret(
    secret_key: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    secret = await get_secret(
        secret_key=secret_key,
        request=request,
        session=session,
    )
    return {"secret": secret}
