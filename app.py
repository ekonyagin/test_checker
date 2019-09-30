import datetime
from flask import Flask, render_template, request, session
import requests
import json
import socket
from collections import OrderedDict
import os
import pandas as pd
import checker
from transliterate import translit, get_available_language_codes

app = Flask(__name__)
app.secret_key = os.urandom(64).hex()

def ParseAnswerString(ans_str):
    Answers = set()
    for i in str(ans_str):
        try:
            if int(i) > 0 and int(i) < 10:
                Answers.add(i)
        except:
            pass
    return Answers

@app.route('/')
def index():
    return render_template('answer_form.html')

@app.route('/set_ans')
def set_ans():
    return render_template('set_ans.html')

@app.route('/root')
def student():
    return render_template('index.html')

@app.route('/submit_answers')
def submit():
    
    first_name = translit(request.args.get("first_name").lower(), 'ru', reversed = True)
    surname = translit(request.args.get("surname").lower(), 'ru', reversed = True)
    email = request.args.get("email").lower()
    class_n = request.args.get("class")
    topic = request.args.get("test_name")
    var = request.args.get("variant")
    answers = OrderedDict()
    for i in range(10):
        a = request.args.get("q"+str(i+1))
        answers["q"+str(i+1)] = ParseAnswerString(a)
    print(answers, surname, first_name, email, class_n, topic, var)
    #with open(name + ".json", "w") as f:
    #    ans = json.dumps(answers)
    #    f.write(ans)
    return(u"Ответ записан")

if __name__ == '__main__':
    if os.path.exists('classes_info') == False:
        os.mkdir('classes_info')
        for i in range(8,12):
            os.mkdir('classes_info/class_'+str(i))
        os.mkdir('classes_info/other')
    app.run(host='0.0.0.0',port='5000',debug=False)
