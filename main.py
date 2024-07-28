from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot.chatbot import Bahasa
from chatbot.process import generate_response


class Req(BaseModel):
    query: str
    bahasa: str


app = FastAPI()


@app.post("/chat")
async def root(req: Req):
    res = await generate_response(req.query, Bahasa[req.bahasa.upper()])
    return {
        'res': res
    }

@app.get("/tes")
async def tes():
    return "Halo, ini dari tes"

