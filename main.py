import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/')
def index():
    return "OK"

@app.route('/acc', methods = ['GET', 'POST'])
def signin():
    try:
        conn = mysql.connect()
        json_ = request.json
        username = json_['username']
        password = json_['password']
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rc = cursor.execute("SELECT * from account WHERE username = %s", (username))
        res = cursor.fetchall()
        if rc == 0:
            d = {"result":"fail", "message":"no username found"}
            return jsonify(d)
        if password != res[0]['pass']:
            d = {"result":"fail", "message":"wrong password"}
            return jsonify(d)     
        d = {"username":username, "result":"ok"}
        return jsonify(d)
    except Exception as e:
        return jsonify(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
@app.route('/signUp', methods= ['GET', 'POST'])
def createAcc():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        password = json_['password']
        name = json_['name']
        email = json_['email']
        rc = cursor.execute("select * from account where username = %s or email = %s", (username, email))
        if rc != 0:
            d = {"result":"fail", "message": "username or email exist"}
            return jsonify(d)
        cursor.execute("insert into account (username, pass, email, name_) values (%s, %s, %s,%s)", (username, password, email, name))
        conn.commit()
        return jsonify({"result":"ok"})
    except Exception as e:
        return jsonify(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run()
