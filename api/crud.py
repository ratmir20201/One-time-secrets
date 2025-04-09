import uuid

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from encryption import encrypt_secret
from models import Secret, SecretLog
from schemas import SecretCreateRequest


async def create_secret(
    secret_data: SecretCreateRequest,
    request: Request,
    session: AsyncSession,
) -> str:
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
):
    pass
