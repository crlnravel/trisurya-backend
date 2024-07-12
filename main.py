from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot.chatbot import Bahasa
from chatbot.process import generate_response


class Req(BaseModel):
    query: str
    bahasa: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trisurya-ui.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def root(req: Req):
    res = await generate_response(req.query, Bahasa[req.bahasa.upper()])
    return {
        'res': res
    }
