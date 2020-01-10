from flask import Flask, render_template, request

app = Flask(__name__)

from BOT import *

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    return str(Discounts(userText.lower())) 


if __name__ == "__main__":
    app.run()
