from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.models import ShortenUrlSchema
from fastapi.staticfiles import StaticFiles
from app.db import database, engine, metadata
from app.api import shorten, db_manager
from fastapi.openapi.utils import get_openapi
import random


metadata.create_all(engine)
app = FastAPI(root_path="/app/", docs_url="/docs")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()




@app.get("/")
async def read_items(request: Request):
    host = request.client.host
    return JSONResponse(content={'title': 'myapp', 'host': host})



@app.get("/redir/{url}", response_model=ShortenUrlSchema)
async def redir(url: str):
    item = await db_manager.get_origin(url)
    
    if item:
        item = dict(item)
        return RedirectResponse(item['origin'])
    else:
        return RedirectResponse("/")

app.include_router(shorten.router, prefix="/shorten", tags=["short"])