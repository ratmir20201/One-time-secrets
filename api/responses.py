def generate_response(description: str, detail: str):
    return {
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


secret_not_found_response = generate_response(
    description="Секрет не найден.",
    detail="Данный секрет не найден.",
)

secret_is_expired_response = generate_response(
    description="Срок жизни секрета истек.",
    detail="Данный секрет больше не доступен (срок действия истек).",
)

secret_already_was_read_response = generate_response(
    description="Секрет был прочитан.",
    detail="Данный секрет уже был прочитан ранее.",
)

incorrect_passphrase_response = generate_response(
    description="Неверная фраза-пароль.",
    detail="Была введена неверная фраза-пароль.",
)

incorrect_data_response = generate_response(
    description="Некорректные данные.",
    detail="Были введены некорректные данные.",
)
