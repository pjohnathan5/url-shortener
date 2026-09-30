from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import random 
import string 


app = FastAPI() 

db = {}
def generate_code():
    chars = string.ascii_letters + string.digits
    code = "".join(random.choices(chars, k=6))
    return code


@app.get("/") 
def test():
    return {"hello": "world" } 

@app.get("/greet/{name}")
def greet(name: str, loud: bool):
    if loud == True: 
        print("this is a query param")
    return {"hello": f"{name}"}

class LinkCreate(BaseModel): 
    long_url: str 

class LinkOut(BaseModel): 
    long_url : str
    short_code: str 

@app.post("/links",response_model=LinkOut)
def create_link(link:LinkCreate): 
    code = generate_code()
    db[code] = link.long_url
    return LinkOut(long_url=link.long_url, short_code=code) 

@app.get("/{code}")
def redirect_link(code:str):
    if code in db: 
        long_url = db[code]
        return RedirectResponse(url=long_url)
    else: 
        raise HTTPException(status_code=404, detail="not found")















