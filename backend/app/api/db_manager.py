from app.api.models import ShortenUrlSchema, UrlDB
from app.db import urls, database


async def post(payload: ShortenUrlSchema):
    query = urls.insert().values(origin=payload.origin, shorten=payload.shorten)
    return await database.execute(query=query)


async def get(origin: str):
    query = urls.select().where(origin == urls.c.origin)
    return await database.fetch_one(query=query)


def get_origin(shorten: str):
    query = urls.select().where(shorten == urls.c.shorten)
    return database.fetch_one(query=query)


async def get_all():
    query = urls.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: ShortenUrlSchema):
    query = (
        urls
        .update()
        .where(id == urls.c.id)
        .values(origin=payload.origin, shorten=payload.shorten)
        .returning(urls.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = urls.delete().where(id == urls.c.id)
    return await database.execute(query=query)
