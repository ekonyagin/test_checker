import datetime
from flask import Flask, render_template, request, session
import requests
import json
import socket
from collections import OrderedDict
import pandas as pd
import checker

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_ans')
def set_ans():
    return render_template('set_ans.html')

@app.route('/student')
def student():
    return render_template('answer_form.html')

@app.route('/submit')
def submit():
    answers = OrderedDict()
    for i in range(10):
        name = request.args.get("test_name")
        a = request.args.get("q"+str(i+1))
        answers["q"+str(i+1)] = a
    with open(name + ".json", "w") as f:
        ans = json.dumps(answers)
        f.write(ans)
    return("Successfully saved")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=False)
