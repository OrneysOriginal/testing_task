from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import delete_table, create_table
from shortener.router import shortener_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_table()
    await create_table()
    print('On')
    yield
    print('Off')


app = FastAPI(
    lifespan=lifespan,
)


app.include_router(
    shortener_router,
)
