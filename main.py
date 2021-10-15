import foo
from fastapi import FastAPI, Request,Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
# from hazm import *


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:8100",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates/")





    
    
    
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/s/{s}")
def read_root(s: str, request: Request):
    # client_host = request.client.host
    a = foo.amir(s)
    return { "s": a}



@app.get("/")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post("/")
def form_post(request: Request):
    result = foo.similar("ببر")
    # return{"message": "Amir is here"}
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

# @app.get("/rest")
# def read_item(num: int):
#     result = spell_number(num)
#     return {"number_spelled": result}



@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/list/{item_id}")
def read_root(item_id: str, request: Request):
    # client_host = request.client.host
    a = foo.similar(item_id)
    return { "item_id": a}