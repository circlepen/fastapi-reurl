from pydantic import BaseModel



class ShortenUrlSchema(BaseModel):
    origin: str
    shorten: str


class UrlDB(ShortenUrlSchema):
    id: int
