from flask import Flask, jsonify, abort, make_response
from flask import request

import MySQLdb as mdb

app = Flask(__name__)  # create the Flask app

db = mdb.connect("129.115.27.67", "iuq276", "kyYstgM5lpci8YaCxT4R", "iuq276")

curs = db.cursor()

app.config["JSON_SORT_KEYS"] = False


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello')
def hello():
    return '[{"message":"hello yourself"}]'


@app.route('/properties', methods=['GET', 'POST'])
def props():
    if request.method == 'GET':
        # curs = db.cursor()
        try:
            curs.execute("SELECT * FROM usprops")
            rv = curs.fetchall()
            l = []
            for result in rv:
                content = {'id': result[0], 'address': result[1], 'city': result[2], 'state': result[3], 'zip': result[4]}
                l.append(content)

            return jsonify(l)

        except:
            return "Error, unable to fetch properties"
        curs.close()
        db.close()

    elif request.method == 'POST':
        addr = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        try:
            query = "INSERT INTO usprops(address, city, state, zip) values (%s, %s, %s, %s)"
            args = (addr, city, state, zip)
            curs.execute(query, args)
            return "added"
        except:
            return "something went wrong"
        curs.close()
        db.close()

    elif request.method == 'POST':
        data = request.get_json()
        addr = data['address']
        city = data['city']
        state = data['state']
        zip_code = data['zip']

        try:
            query = "INSERT INTO usprops(address, city, state, zip) values (%s, %s, %s, %s)"
            args = (addr, city, state, zip_code)
            curs.execute(query, args)
            db.commit()
            return "added"
        except:
            return "something went wrong"
        curs.close()
        db.close()

    else:
        return "NOT GET OR POST"


@app.route('/properties/<req_id>', methods=['GET', 'DELETE'])
def get_id(req_id):
    if request.method == 'GET':
        try:
            query = "SELECT * FROM usprops where id = %s"
            curs.execute(query, req_id)

            rv = curs.fetchall()
            l = []
            for result in rv:
                content = {'id': result[0], 'address': result[1], 'city': result[2], 'state': result[3], 'zip': result[4]}
                l.append(content)

            return jsonify(l)

        except:
            return "Error, unable to fetch properties"
    elif request.method == 'DELETE':
        try:
            query = "DELETE FROM usprops where id = %s"
            curs.execute(query, req_id)
            db.commit()
            return "deleted successfully"
        except:
            return "something went wrong"

@app.route('/properties/<id>', methods=['GET', 'DELETE'])
def get_id(req_id):
    if request.method == 'GET':
        try:
            query = "SELECT * FROM usprops where id = %s"
            curs.execute(query, req_id)

            rv = curs.fetchall()
            l = []
            for result in rv:
                content = {'id': result[0], 'address': result[1], 'zip': result[2]}
                l.append(content)

            return jsonify(l)

        except:
            return "Error, unable to fetch properties"
    elif request.method == 'DELETE':
        try:
            query = "DELETE FROM usprops where id = %s"
            curs.execute(query, req_id)
            return "deleted"
        except:
            return "something went wrong"




if __name__ == '__main__':
    app.run()
