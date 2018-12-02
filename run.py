from flask import Flask
from flask import render_template, request, redirect, url_for, session, escape
from flask_cors import CORS
import json
import pymysql
import os
import smtplib
from email.mime.text import MIMEText

PWD = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, template_folder="static/templates", static_folder="static")
id = {}
# <------ error hander---------->

@app.errorhandler(500)
def internal_error(error):

    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

#<------------------------------>

#<--------cors permission settins----------->

cors = CORS(app, resources={
  r"/*": {"origin": "*"},
})

#<------------------------------------------>
def getConnection():
    return pymysql.connect(host='54.244.72.128', user='root', password='1234',
                           db='InterviewNet', charset='utf8')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # session key

@app.route('/signIn')
def signIn():
    render_template('signin.html')

@app.route('/logIn', methods=['GET','POST'])
def logIn():
    if request.method == 'POST':
        conn = getConnection()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        jsonObj = request.get_json()
        sql = "select userpw from Member where userid = %s"
        curs.execute(sql, (jsonObj["userid"]))
        result = curs.fetchone()
        conn.commit()
        print("getUserPW success")
        if result == jsonObj["userpw"]:
            session['userid'] = jsonObj["userid"]
            return redirect(url_for('/index'))
    return redirect(url_for('/index'))


@app.route('/logOut')
def logOut():
    # remove the username from the session if its there
    session.pop('userid', None)
    return redirect(url_for('/'))

@app.route('/idExist', methods=['POST'])
def idExist():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()
    getId = jsonObj["userid"]
    print (jsonObj)
    sql = "select id from Member"
    id = curs.fetchall()
    result = "true"
    for i in id:
        if getId == i:
            result = "false"
            result = json.dumps(result)
            return result
    conn.commit()
    conn.close()
    result = json.dumps(result)
    return result

@app.route('/nickExist', methods=['POST'])
def nickExist():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()
    getNickname = jsonObj["nickname"]
    print (jsonObj)
    sql = "select nickname from Member"
    nickname = curs.fetchall()
    result = "true"
    for i in nickname:
        if getNickname == i:
            result = "false"
            result = json.dumps(result)
            return result
    conn.commit()
    conn.close()
    return result

@app.route('/setSignUp', methods=['POST'])
def setSignUp():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()
    print (jsonObj)
    sql = "insert into Member(userid, userpw, city, college, major, town, nickname, username, point, birth, randNum) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    curs.execute(sql,(jsonObj["userid"], jsonObj["userpw"], jsonObj["city"], jsonObj["college"], jsonObj["major"], jsonObj["town"], jsonObj["nickname"], jsonObj["username"], jsonObj["point"], jsonObj["birth"], jsonObj["randNum"]))
    conn.commit()
    print ("setSignUp success")
    conn.close()
    return redirect(url_for('/index'))

@app.route('/sign_up')
def sign_up():
    return render_template("signup.html")

@app.route('/')
def main():
    if 'userid' in session:
        return 'Logged in as %s' % escape(session['userid'])
    return render_template("main.html")


@app.route('/sendQuestionOption', methods = ['PUT'])
def getQuestion():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()

    print(jsonObj)
    sql = "SELECT * FROM Question WHERE major=%s and company=%s"
    curs.execute(sql, (jsonObj["occupation"], jsonObj["company"]))
    results = {}
    results = curs.fetchall()
    jsonObj = json.dumps(results)
    conn.commit()
    print (jsonObj)
    print("getQuestion success.")
    conn.close()
    return jsonObj


@app.route('/question')
def question():
    return render_template("question.html")

@app.route('/matching')
def matching():
    return render_template("matching.html")

@app.route('/getMemberInfo', methods=['PUT'])
def getMemberInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()
    print (jsonObj)
    sql = "select * from Matching where company = %s and city = %s and town = %s and major = %s"
    curs.execute(sql,(jsonObj["company"], jsonObj["city"], jsonObj["town"], jsonObj["major"]))
    results = curs.fetchall()
    jsonObj = json.dumps(results)
    conn.commit()
    print (jsonObj)
    print ("getMemberInfo success")
    conn.close()
    return jsonObj

@app.route('/setMember', methods=['POST'])
def setMember():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()
    print (jsonObj)
    sql = "insert into Matching(username, city, town, company, major, userInfo) values(%s, %s, %s, %s, %s, %s)"
    curs.execute(sql,(jsonObj["username"], jsonObj["city"], jsonObj["town"], jsonObj["company"], jsonObj["major"], jsonObj["userInfo"]))
    conn.commit()
    print ("setMember success")
    conn.close()
    return redirect(url_for('matching'))

@app.route('/studyroom')
def studyroom():
    return render_template("studyroom.html")

@app.route('/community')
def community():
    return render_template("community.html")

@app.route('/write')
def write():
    return render_template("write.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/mypage')
def mypage():
    return render_template("mypage.html")

@app.route('/post')
def post():
    return render_template("post.html")

@app.route('/getPostInfo', methods=['GET'])
def getPostInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "select * from Info where id = %s"
    global id
    curs.execute(sql, (id))
    results = curs.fetchone()
    jsonObj = json.dumps(results)
    conn.commit()
    print ("getPostInfo success")
    conn.close()
    return jsonObj


@app.route('/getInfo', methods=['GET'])
def getInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from Info order by id desc"
    curs.execute(sql)
    results = curs.fetchall()
    jsonObj = json.dumps(results)
    conn.commit()
    print (jsonObj)
    print ("getInfo success")
    conn.close()
    return jsonObj

@app.route('/writeInfo', methods=['POST'])
def writeInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()

    print (jsonObj)
    sql = "insert into Info(author, title, text, time, hit) values(%s, %s, %s, %s, %s)"
    curs.execute(sql, (jsonObj["sid"], jsonObj["stitle"], jsonObj["stext"], jsonObj["stime"], jsonObj["sview"]))
    conn.commit()
    print ("writeInfo success")
    conn.close()
    return redirect(url_for('community'))

@app.route('/clickInfo', methods=['PUT'])
def clickInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    jsonObj = request.get_json()

    print (jsonObj)
    sql = "select hit from Info where id = %s"
    curs.execute(sql, (jsonObj["id"]))
    sql = "update Info set hit = %s where id = %s"
    curs.execute(sql, (jsonObj["sview"], jsonObj["id"]))
    conn.commit()
    print ("clickInfo success")
    global id
    id = jsonObj["id"]
    conn.close()
    return redirect(url_for('post'))


@app.route('/reviseInfo', methods=['PUT'])
def reviseInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    return 1

@app.route('/delInfo', methods=['DELETE'])
def delInfo():
    conn = getConnection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    return 1

@app.route('/sendEmail', methods=['POST'])
def sendEmail():
    smtp = smtplib.SMTP('smtp.live.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    collegeMail = ''
    id = ''
    smtp.login('kmswin7@gmail.com', '1234')

    msg = MIMEText('본문 테스트 메시지')
    msg['Subject'] = '테스트'
    msg['To'] = id+'@'+collegeMail
    smtp.sendmail('kmswin7@gmail.com', id+'@'+collegeMail , msg.as_string())

    smtp.quit()


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
