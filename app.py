from flask import Flask, request
import json
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Home Page"

import controller.search_controller as search_controller
import controller.movies_controller as movies_controller

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
	

