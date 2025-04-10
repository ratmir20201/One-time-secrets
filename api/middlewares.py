from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class NoCacheMiddleware(BaseHTTPMiddleware):
    """Middleware для запрета кэширования на клиенте."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Функция переопределенная из BaseHTTPMiddleware."""

        response: Response = await call_next(request)

        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response
