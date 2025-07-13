import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# FastAPI always returns a JSON response by default
# To return HTML, we need to specify the response class

BASE_DIR = pathlib.Path(__file__).parent
print( BASE_DIR/ "templates" )
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    return templates.TemplateResponse({"request": request}, "home.html",{ "developer": "MadhushankhaDeS"})

@app.post("/")
def home_detail_view():
    return {"message": "Welcome to the FastAPI application!"}