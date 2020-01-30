from flask import Flask, jsonify, abort, make_response
from flask import request
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql
import MySQLdb as mdb
from flaskext.mysql import MySQL
import jaydebeapi


app = Flask(__name__) #create the Flask app

db = mdb.connect("129.115.27.67", "iuq276", "kyYstgM5lpci8YaCxT4R", "iuq276")

curs = db.cursor()

app.config["JSON_SORT_KEYS"] = False

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello')
def hello():
    return '[{"message":"hello yourself"}]'

@app.route('/properties',  methods=['GET', 'POST'])
def props():
    if request.method == 'GET':
        #curs = db.cursor()
        try:
            curs.execute("SELECT * FROM usprops")
            rv = curs.fetchall()
            l = []
            for result in rv:
                content = {'id': result[0], 'address': result[1], 'zip': result[2]}
                l.append(content)

            return jsonify(l)

        except:
            return "Error, unable to fetch properties"
        curs.close()
        db.close()

    else:
        return "man"



if __name__ == '__main__':

    app.run()
