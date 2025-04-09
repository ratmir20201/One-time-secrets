from cryptography.fernet import Fernet

from config import settings

fernet = Fernet(settings.crypto.fernet_key)


def encrypt_secret(secret: str) -> str:
    return fernet.encrypt(secret.encode()).decode()
