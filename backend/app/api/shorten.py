from fastapi import APIRouter
from app.api.models import ShortenUrlSchema, UrlDB
from app.api import db_manager
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
import random

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("URLInputPage.html", {'request': request})

def create_url():
    chars = '0123456789ABCDEFGIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ans = ''
    for i in range(8):
        ans += random.choice(chars)
    return ans

@router.post("/", response_model=ShortenUrlSchema)
async def shorten_func(url: str =  Form(...)):
    exist_url = await db_manager.get(url)
    if exist_url:
        return exist_url
    else:
        chars = '0123456789ABCDEFGIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        new_url = create_url()
        new_object = ShortenUrlSchema(origin=url, shorten=new_url)
        await db_manager.post(new_object)
        response_object = {
            "origin": str(new_object.origin),
            "shorten": str(new_object.shorten)
        }
    return response_object
