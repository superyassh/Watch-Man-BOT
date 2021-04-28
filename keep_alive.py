from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "<H1> Minor Project </H1> <p><BR> Discord BOT is online </p><BR> Created by @superyassh, @pavbyte & Team "

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()