from app.api import db_manager, shorten
from app.api.models import ShortenUrlSchema
from app.auth import auth as auth_routes
from app.auth.auth import get_current_active_user, get_current_user
from app.db import database, engine, metadata
from fastapi import (APIRouter, FastAPI)
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

metadata.create_all(engine)
app = FastAPI(root_path="/", docs_url="/docs")

app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_items():
    return RedirectResponse("shorten/")



@app.get("/redir/{url}", response_model=ShortenUrlSchema)
async def redir(url: str):
    item = await db_manager.get_origin(url)

    if item:
        item = dict(item)
        url = item['origin']
        if 'http' or 'https' not in url:
            url = 'http://' + url

        return RedirectResponse(url)
    else:
        return RedirectResponse("/")

# @app.get("/users/me")
# async def read_users_me(current_user = Depends(get_current_active_user)):
#     return current_user

# async def get_items(
#     current_user = Security(get_current_user, scopes=["items"])
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.get("/users/items")
# async def read_user_items(current_user = Depends(get_items)):
#     return {1:{"user": 'Lyle'}, 2: {'user': 'Tom'}}


app.include_router(shorten.router, prefix="/shorten", tags=["short"])
# app.include_router(auth_routes.router)
