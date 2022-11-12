import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/')
def index():
    return "deploy success"

@app.route('/acc', methods = ['GET'])
def signin():
    try:
        conn = mysql.connect()
        json_ = request.json
        username = json_['username']
        password = json_['password']
        IP = json_['IP']
        port = json_['port']
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rc = cursor.execute("SELECT * from account WHERE username = %s and pass = %s", (username, password))
        if rc == 0:
            return jsonify("not ok")
        rc = cursor.execute("UPDATE account set IP = %s, Port = %s, STATUS = %s WHERE username = %s", (IP, port, "on", username))
        conn.commit()
        return jsonify("OK")
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/acc', methods = ['POST'])
def signup():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        name = json_['name']
        username = json_['username']
        password = json_['password']
        rc = cursor.execute("INSERT INTO account (name, username, pass) values (%s, %s,%s)", (name,username, password))
        conn.commit()
        if rc == 0:
            reponse = jsonify("not ok")
            return reponse
        return jsonify("OK")
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
        rc = cursor.execute('UPDATE account set STATUS = %s WHERE username = %s', ("off", username))
        if rc == 0:
            return jsonify("not ok")
        return jsonify("OK")
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@app.route('/getIP', methods = ['GET'])
def getIP():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        json_ = request.json
        username = json_['username']
        rc = cursor.execute("SELECT IP, port FROM account WHERE username = %s", username)
        if rc == 0:
            return jsonify("not ok")
        res = cursor.fetchall()
        return jsonify(res)
    except Exception as e:
        print(e)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run()