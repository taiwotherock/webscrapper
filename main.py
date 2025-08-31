from ast import And
from typing import Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chainlit.utils import mount_chainlit
import os

from dotenv import load_dotenv

load_dotenv()



app = FastAPI()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

mount_chainlit(app=app, target="app.py", path="/chainlit")