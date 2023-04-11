from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
from chatbot_net import getResponse
from gpt4_cakebot import get_gpt4_Response

@app.route("/chatbot", methods=["POST", "GET"])
def chatbot():
    message = request.data.decode("utf-8")
    response = getResponse(message)
    return jsonify({'response': response})


@app.route("/gpt4", methods=["POST","GET"])
def gptbot():
    message = request.data.decode("utf-8")
    response = get_gpt4_Response(message)
    return jsonify({'response': response})


if __name__=="__main__":
    app.run(debug=True)