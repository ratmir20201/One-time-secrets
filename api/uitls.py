import datetime

from fastapi import HTTPException
from starlette.status import HTTP_410_GONE

from models import Secret


async def check_secret_is_alive(secret: Secret) -> None:
    """Функция для проверки срока жизни секрета."""

    current_time = datetime.datetime.now(datetime.UTC)
    expiration_time = secret.created_at + datetime.timedelta(seconds=secret.ttl_seconds)

    if current_time > expiration_time:
        raise HTTPException(
            status_code=HTTP_410_GONE,
            detail="Данный секрет больше не доступен (срок действия истек).",
        )
