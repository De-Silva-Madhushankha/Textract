import io
import pathlib
import os
import uuid
from functools import lru_cache
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile,)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
from PIL import Image
import pytesseract

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = True

    model_config = {
        "env_file": ".env",}

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG = settings.debug


BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# FastAPI always returns a JSON response by default
# To return HTML, we need to specify the response class
@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse({"request": request}, "home.html",{ "developer": "MadhushankhaDeS", })

@app.post("/")
async def prediction_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):

    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")
    preds = pytesseract.image_to_string(img)
    predictions = [x for x in preds.split("\n") if x.strip()]
    return {"predictions": predictions, "original": preds}


@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(status_code=400, detail="Echo is not active")
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}" # To avoid filename conflicts
    img.save(dest)
    return dest