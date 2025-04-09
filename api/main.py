import uvicorn
from fastapi import FastAPI

from api.routes import router
from db import engine, Base


async def lifespan(app: FastAPI):
    """Перед запуском приложения создает базу данных, а после удаляет ее."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
