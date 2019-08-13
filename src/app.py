import sys
from flask import Flask, render_template, request, redirect, Response
import random, json
from sheet_generator import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json(force=True)
    data = data[0]
    print(data)
    
    scanVideo(data["url"], data["color"])

    return "test"
    # return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
