from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_410_GONE,
    HTTP_403_FORBIDDEN,
)

from responses import (
    incorrect_data_response,
    secret_not_found_response,
    secret_is_expired_response,
    secret_already_was_read_response,
    incorrect_passphrase_response,
)

create_secret_responses = {
    HTTP_400_BAD_REQUEST: incorrect_data_response,
}

get_secret_responses = {
    HTTP_403_FORBIDDEN: secret_already_was_read_response,
    HTTP_404_NOT_FOUND: secret_not_found_response,
    HTTP_410_GONE: secret_is_expired_response,
}

delete_secret_responses = {
    HTTP_400_BAD_REQUEST: incorrect_passphrase_response,
    HTTP_404_NOT_FOUND: secret_not_found_response,
    HTTP_410_GONE: secret_is_expired_response,
}
