from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging


from ..crud.models import *
from .routers import users, words, user_words, word_relations

app = FastAPI()
origins = [
    "http://localhost:5173",  # your React frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],  # important: allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app.include_router(users.user_router)
app.include_router(words.word_router)
app.include_router(user_words.user_word_router)
app.include_router(word_relations.word_relation_router)

