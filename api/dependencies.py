from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from crud import get_secret
from db import get_session
from models import Secret
from uitls import check_secret_is_alive


async def secret_by_secret_key(
    secret_key: str,
    session: AsyncSession = Depends(get_session),
) -> Secret:
    """Зависимость для получения привычки по ее id."""
    secret = await get_secret(secret_key=secret_key, session=session)

    if secret is not None:
        await check_secret_is_alive(secret)
        return secret

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Данный секрет не найден.",
    )
