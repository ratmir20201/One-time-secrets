import uuid

from fastapi import Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from api.encryption import decrypt_secret
from api.uitls import check_secret_is_alive
from encryption import encrypt_secret
from models import Secret, SecretLog
from schemas import SecretCreateRequest


async def create_secret(
    secret_data: SecretCreateRequest,
    request: Request,
    session: AsyncSession,
) -> str:
    """
    Метод для создания объета Secret.

    Сам секрет мы шифруем и создаем объект Secret.
    Также создаем объект SecretLog для логирования.
    """
    secret_key = str(uuid.uuid4())

    encrypted_secret = encrypt_secret(secret_data.secret)

    new_secret = Secret(
        key=secret_key,
        secret=encrypted_secret,
        passphrase=secret_data.passphrase,
        ttl_seconds=secret_data.ttl_seconds,
    )
    new_secret_log = SecretLog(
        ip_address=request.client.host,
        action="create",
        secret_key=new_secret.key,
    )

    session.add(new_secret)
    session.add(new_secret_log)
    await session.commit()

    return secret_key


async def get_secret(
    secret_key: str,
    request: Request,
    session: AsyncSession,
) -> Secret.secret:
    """
    Метод для получения объета Secret по его key.

    Проверяем существует ли такой секрет, и не был ли он еще прочитан.
    Также создаем объект SecretLog для логирования.
    Отправляем расшифрованный секрет (конфиденциальные данные).
    """
    secret_query = await session.execute(select(Secret).where(Secret.key == secret_key))
    secret = secret_query.scalar_one_or_none()

    if not secret:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Данный секрет не найден.",
        )

    if secret.was_read:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Данный секрет уже был прочитан ранее.",
        )

    await check_secret_is_alive(secret)

    new_secret_log = SecretLog(
        ip_address=request.client.host,
        action="read",
        secret_key=secret_key,
    )

    session.add(new_secret_log)
    await session.commit()

    decrypted_secret = decrypt_secret(secret.secret)

    return decrypted_secret
