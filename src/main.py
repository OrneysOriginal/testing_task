from fastapi import FastAPI

from src.shortener.router import shortener_router


app = FastAPI()

app.include_router(
    shortener_router,
)
