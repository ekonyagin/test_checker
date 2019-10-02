import datetime
from flask import Flask, render_template, request, session
import requests
import json
import socket
from collections import OrderedDict
import os
import pandas as pd
import mail_sender
from transliterate import translit, get_available_language_codes
import sys
import stat_creator

app = Flask(__name__)
app.secret_key = os.urandom(64).hex()

def Score(ans,correct_ans):
    if(len(ans - correct_ans)) !=0 or len(ans) == 0:
        return 0
    if ans == correct_ans:
        return 2
    else:
        return 1

def ApplyScore(answers, test_name,class_n, var):
    try:
        with open('correct_answers/'+test_name+"_"+str(class_n)+"_"+str(var)+'.json') as json_file:
            raw_answers = json.load(json_file)
            print(raw_answers)
            correct_answers = {}
            for i in range(10):
                a = raw_answers["q"+str(i+1)]
                correct_answers["q"+str(i+1)] = ParseAnswerString(a)
    except:
        return -1
    score = 0
    for i in range(10):
        score += Score(answers['q'+str(i+1)], correct_answers["q"+str(i+1)])
    return score

def CheckExistence(surname, first_name, class_n):
    if os.path.exists("classes_info/class"+str(class_n)+"/"+ surname+"_"+first_name+".json"):
        return True
    return False

def InitializeUser(surname, first_name, class_n):
    data = {
        "surname" : surname,
        "first_name" : first_name,
        "class_n" : class_n,
        "tests" : []
    }
    try:
        fname = "classes_info/class"+str('class_n')+"/"+ 'surname'+"_"+'first_name'+".json"
        with open(fname, 'w') as f:
            json.dump(data, f)
        return 0
    except:
        return -1

def SaveAns(query, score):
    if CheckExistence(query['surname'], query['first_name'], query['class_n'])==True:

        fname = "classes_info/class"+str(query['class_n'])+"/"+ query['surname']+"_"+query['first_name']+".json"
        f = open(fname, 'r')
        data = json.load(f)
        f.close()
        test = {'topic' : query['topic'],
                    'class' : query['class_n'],
                    'variant' : query['var'],
                    'answers' : query['ans'],
                    'score' : score}
        data['tests'].append(test)
        with open(fname, 'w') as f:
            json.dump(data, f)
        return 0
    else:
        code = InitializeUser(query['surname'], query['first_name'], query['class_n'])
        return code

def CreateTest(query):
    pass
    try:
        test_name = query.get('test_name')
        class_n = query.get("class")
        variant = query.get("variant")
        deadline = query.get("deadline")
        answers = {}
        for i in range(10):
            a = query.get("q"+str(i+1))
            answers["q"+str(i+1)] = a
        print(answers)
        with open('correct_answers/'+test_name+"_"+str(class_n)+"_"+str(variant)+'.json', "w") as json_file:
            json.dump(answers, json_file)
        return 0
    except Exception as e:
        print(e)
        return -1

def Initialize():
    try:
        if os.path.exists('classes_info') == False:
            os.mkdir('classes_info')
            for i in range(8,12):
                os.mkdir('classes_info/class_'+str(i))
            os.mkdir('classes_info/other')

        if os.path.exists('correct_answers') == False:
            os.mkdir('correct_answers')
        return 0
    except:
        return -1

def ParseAnswerString(ans_str):
    Answers = set()
    for i in str(ans_str):
        try:
            if int(i) > 0 and int(i) < 10:
                Answers.add(i)
        except:
            pass
    return Answers

def ProceedQuery(query):
    if query['first_name'] and query['surname']:

        class_n = query['class_n']
        return 0
    else:
        return -1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    email = sys.argv[1]
    send = sys.argv[2]==1
    try:
        session['key'] = mail_sender.CreateAccessCode(email,send)
        return render_template("root_login_sent_code.html")
    except Exception as e:
        print(e)
        return u'Произошла ошибка. Обратитесь к администратору.'

@app.route('/submit_answers')
def submit():
    query = OrderedDict()
    query['first_name'] = translit(request.args.get("first_name").lower(), 'ru', reversed = True)
    query['surname'] = translit(request.args.get("surname").lower(), 'ru', reversed = True)
    query['email'] = request.args.get("email").lower()
    query['class_n'] = request.args.get("class")
    query['topic'] = request.args.get("test_name")
    query['var'] = request.args.get("variant")
    answers = OrderedDict()
    for i in range(10):
        a = request.args.get("q"+str(i+1))
        answers["q"+str(i+1)] = ParseAnswerString(a)
    query['ans'] = answers
    print(query)
    
    score = ApplyScore(query['ans'], query['topic'], query['class_n'], query['var'])
    if score == -1:
        return(u"Не удалось проверить тест. Убедитесь, что правильно выбраны тема теста (вариант) и отправьте еще раз.")
    else:
        SaveAns(query, score)
        try:
            mail_sender.SendResEmail(query['email'], score, query['topic'])
        except:
            print("error with email_sending")
        return(u"Вы набрали за данный тест "+str(score) +" баллов из 20. Результаты отправлены на указанный email")

    if ProceedQuery(query)==-1:
        return(u"Не заданы имя или фамилия. Отправьте еще раз!")
    
    return(u"Ответ записан")

@app.route('/root/login')
def root_login():
    return render_template('root_login.html')

@app.route('/root/login', methods = ['POST'])
def proceed_login():
    login_data = request.form
    pwd = login_data.get('pwd')
    print(pwd)
    if session.get('key') != None:
        if pwd == session['key']:
            session['logged'] = True
            return render_template('root_index.html')
        else:
            return("Неправильный код доступа!")
    else:
            return("Неправильный код доступа!")
    

@app.route('/root/logout')
def proceed_logout():
    session['logged'] = False
    session.pop('key')
    return "Вы успешно вышли из личного кабинета"

@app.route('/root/set_ans')
def set_ans():
    if session.get('key') != None:
        if session['logged'] == True:
            return render_template('set_ans.html')
        else:
            return render_template('root_login.html')
    else:
            return render_template('root_login.html')

@app.route('/root/set_ans/submit', methods= ['POST'])
def create_test():
    if session.get('key') != None:
        if session['logged'] == True:
            if CreateTest(request.form) == 0:
                return u"Успешно сохранено!"
            else:
                return u"Произошла ошибка. Попробуйте еще раз"
        else:
            return render_template('root_login.html')
    else:
            return render_template('root_login.html')


@app.route('/root')
def root_page():
    if session.get('logged') != None:
        if session['logged'] == True:
            return render_template('root_index.html')
    return render_template('root_login.html')

@app.route('root/view_stat_class')
def stat_class():
    if session.get('key') != None:
        if session['logged'] == True:
            return render_template("root_stat_class.html")
        else:
            return "Access denied!"
    else:
            return "Access denied!"

@app.route('/root/view_stat_class/submit', methods = ['POST'])
def create_stat():
    args = request.form

@app.route('/root/view_stat_student')
def stat_student():
    if session.get('key') != None:
        if session['logged'] == True:
            return render_template("root_stat_student.html")
        else:
            return "Access denied!"
    else:
            return "Access denied!"


if __name__ == '__main__':
    Initialize()
    app.run(host='0.0.0.0',port='5000',debug=False)
