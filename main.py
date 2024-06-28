from fastapi import FastAPI
from pydantic import BaseModel

from chatbot.chatbot import Bahasa
from chatbot.process import generate_response


class Req(BaseModel):
    query: str
    bahasa: str


app = FastAPI()


@app.post("/")
async def root(req: Req):
    res = await generate_response(req.query, Bahasa[req.bahasa.upper()])
    return {
        'res': res
    }
