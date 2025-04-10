import uvicorn
from fastapi import FastAPI

from middlewares import NoCacheMiddleware
from routes import router

# async def lifespan(app: FastAPI):
#     """Перед запуском приложения создает базу данных, а после удаляет ее."""
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


app = FastAPI()

app.include_router(router)

app.add_middleware(NoCacheMiddleware)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
