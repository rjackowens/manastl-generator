from flask import Flask

app = Flask(__name__)

from src import routes

app.run(host="0.0.0.0", port=8080)
