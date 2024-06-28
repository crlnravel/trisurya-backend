import asyncio

from flask import Flask, request, Response
from flask_cors import CORS

from chatbot.chatbot import Bahasa
from chatbot.process import generate_response

app = Flask(__name__)
CORS(app)


@app.route('/api/chat', methods=['POST'])
def chat():  # put application's code here
    data = request.json

    res = asyncio.run(generate_response(data['query'], Bahasa[data['bahasa'].upper()]))

    return {
        'res': res
    }


if __name__ == '__main__':
    app.run()
