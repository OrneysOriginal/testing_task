from pydantic import BaseModel


class SUrl(BaseModel):
    original_url: str