import pymysql
from flask import Flask, jsonify, abort, Response
from flask import request
from flask_sslify import SSLify
from flask_swagger_ui import get_swaggerui_blueprint
import pymysql.cursors
import sys
from flask_cors import CORS

app = Flask(__name__)  # create the Flask app
CORS(app)
context = ('web.crt', 'web.key')
#sslify = SSLify(app)

# db = mdb.connect("129.115.27.67", "iuq276", "kyYstgM5lpci8YaCxT4R", "iuq276")
db = pymysql.connect(host='129.115.27.67', user='iuq276', password='kyYstgM5lpci8YaCxT4R', db='iuq276',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor
                     )
curs = db.cursor()

app.config["JSON_SORT_KEYS"] = False

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "assignment2"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


### end swagger specific ###

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

            return jsonify(rv)

        except:
            return Response("Error, unable to fetch properties", status=404, mimetype="application/json")
        curs.close()
        db.close()

    elif request.method == 'POST':
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == 'cs4783FTW':
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
                return Response("something went wrong", status=404, mimetype="application/json")
            curs.close()
            db.close()
        else:
            return jsonify({"message": "ERROR: Unauthorized"}), 401

    else:
        return "NOT GET OR POST"


@app.route('/properties/<req_id>', methods=['GET', 'DELETE', 'PUT'])
def get_id(req_id):
    if request.method == 'GET':
        if not req_id.isdigit():
            return Response("ID IS NOT A NUMBER", status=404, mimetype="application/json")
        try:
            query = "SELECT * FROM usprops where id = %s"
            curs.execute(query, req_id)

            rv = curs.fetchall()
            if not rv:
                abort(404)
            return jsonify(rv)

        except:
            return Response("something went wrong", status=404, mimetype="application/json")
    elif request.method == 'DELETE':
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == 'cs4783FTW':
            if not req_id.isdigit():
                abort(400)
            try:
                query = "DELETE FROM usprops where id = %s"
                curs.execute(query, req_id)
                db.commit()
                return "deleted successfully"
            except:

                return Response("something went wrong", status=404, mimetype="application/json")
        else:
            return jsonify({"message": "ERROR: Unauthorized"}), 401
    elif request.method == 'PUT':
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth == 'cs4783FTW':
            if not req_id.isdigit():
                abort(400)
            data = request.get_json()
            addr = data['address']
            city = data['city']
            state = data['state']
            zip_code = data['zip']

            query = "SELECT * FROM usprops where id = %s"
            curs.execute(query, req_id)

            rv = curs.fetchall()

            if not addr:
                addr = rv.get('address')
            if not city:
                city = rv.get('city')
            if not state:
                state = rv.get('state')
            if not zip_code:
                zip_code = rv.get('zip')

            try:
                query = "Update usprops set address = %s, city =%s, state = %s, zip = %s where id = %s"
                args = (addr, city, state, zip_code, req_id)
                curs.execute(query, args)
                db.commit()
                return "updated"
            except:
                return Response("something went wrong", status=404, mimetype="application/json")
            curs.close()
            db.close()
        else:
            return jsonify({"message": "ERROR: Unauthorized"}), 401


if __name__ == '__main__':
    if sys.argv[1] == 'https' or sys.argv[1] == 'Https':
        #context = ('web.crt', 'web.key')
        app.run(host="0.0.0.0", port=12100, ssl_context='adhoc')
    elif sys.argv[1] == 'http' or sys.argv[1] == 'HTTP':
        app.run(host="0.0.0.0", port=12100)
