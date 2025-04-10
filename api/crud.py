import uuid

from fastapi import Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN

from api.encryption import decrypt_secret
from encryption import encrypt_secret
from models import Secret, SecretLog
from schemas import SecretCreateRequest, SecretDeleteRequest


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


async def get_secret(secret_key: str, session: AsyncSession) -> Secret | None:
    """Функция для получения секрета."""
    secret_query = await session.execute(select(Secret).where(Secret.key == secret_key))
    secret = secret_query.scalar_one_or_none()
    return secret


async def check_secret_and_make_logs(
    secret: Secret,
    request: Request,
    session: AsyncSession,
) -> Secret.secret:
    """
    Метод для получения объекта Secret по его key.

    Проверяем существует ли такой секрет, и не был ли он еще прочитан.
    Также создаем объект SecretLog для логирования.
    Отправляем расшифрованный секрет (конфиденциальные данные).
    """
    if secret.was_read:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Данный секрет уже был прочитан ранее.",
        )

    secret.was_read = True

    new_secret_log = SecretLog(
        ip_address=request.client.host,
        action="read",
        secret_key=secret.key,
    )

    session.add(new_secret_log)
    session.add(secret)
    await session.commit()

    decrypted_secret = decrypt_secret(secret.secret)

    return decrypted_secret


async def delete_secret(
    secret: Secret,
    delete_data: SecretDeleteRequest,
    request: Request,
    session: AsyncSession,
) -> str:
    if secret.passphrase and secret.passphrase != delete_data.passphrase:
        raise HTTPException(
            status_code=403,
            detail="Неверная фраза-пароль.",
        )

    await session.delete(secret)

    new_secret_log = SecretLog(
        ip_address=request.client.host,
        action="delete",
        secret_key=secret.key,
    )

    session.add(new_secret_log)
    await session.commit()

    return "secret_deleted"
