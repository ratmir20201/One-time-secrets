from pydantic import BaseModel


class SecretCreateRequest(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl_seconds: int | None = 300


class SecretCreateResponse(BaseModel):
    secret_key: str


class SecretReadResponse(BaseModel):
    secret: str


class SecretDeleteResponse(BaseModel):
    status: str


class SecretDeleteRequest(BaseModel):
    passphrase: str | None = None
