
# Fast api Imports
from fastapi import FastAPI,Body,Response,HTTPException,status,Depends

# random Numberimport 
from random import randrange

from typing import List
# datetime import
from datetime import datetime, timezone


# import models from SQLalchemy
from . import models 
from app.database import engine,get_db
from sqlalchemy.orm import Session


from .schema import UserCreate,CreatePost,UpdatePost,PostResponse,UserResponse

# importing Hashing From utils.py
from .utils import hash

from app.routes import post,user,auth,password
from fastapi.middleware.cors import CORSMiddleware

# running statement to Create all MOdels From SQLalchemy 
models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)

app.include_router(post.router)
app.include_router(password.router)
# Allow your local frontend files to communicate with your backend port
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def home():
    return {"safe Runningg"}