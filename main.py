import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/')
def index():
    return "OK"

@app.route('/acc', methods = ['GET'])
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
            cursor.execute("insert into account(username,pass, status) values (%s, %s, %s)", (username, password, "on"))
            d = {"username":username, "pass": password, "STATUS":"on", "ID": ""}
            return jsonify(d)
        if password != res[0]['pass']:
            return jsonify("wrong pass")
        cursor.execute("update account set isOnl = 1 where username = %s" , username)
        d = {"username":username, "pass": password, "isOnl": 1 , "ID": res[0]['ID']}
        conn.commit()
        return jsonify(d)
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
            
@app.route('/acc', methods = ['PUT'])
def setOff():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        rc = cursor.execute('update account set isOnl = 0 where username = %s', username)
        if rc == 0:
            return jsonify("not ok")
        return jsonify("OK")
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run()