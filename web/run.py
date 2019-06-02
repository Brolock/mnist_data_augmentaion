from flask import Flask
from flask import request, send_file

import json
import uuid
import os
import hashlib

import mysql.connector

from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():
    return "The Root of all evil!\n"

@app.route("/single_image", methods=["GET", "POST"])
def single_image():
    if request.method == "GET":
        return render_template("query_image.html")
    else:
        user_id = request.form['user_id']
        number = request.form['number']
        unique_id = str(uuid.uuid1())
        channel.basic_publish(exchange='',
                routing_key='web-queries',
                body=json.dumps({"user_id": user_id,"number": number, "query_id": unique_id}))

        return "You enter userid={} and number={}\n".format(user_id, number)

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("create_account.html")
    else:
        username = request.form["user_name"]
        password = request.form["password"]

        hashed_pwd = hashlib.sha256(password.encode())
        cursor.execute("INSERT INTO users (user_name, password) VALUES (%s, UNHEX(%s))",
                       (username, hashed_pwd.hexdigest()))
        cnx.commit()
        return "Welcome {}! Your password is {}, write it down!".format(username, password)

@app.route("/bootstrap.min.css")
def get_bootstram():
    return send_file("templates/bootstrap.min.css")

#TODO MOVE ELSWHERE
def get_env(env_var):
    if env_var in os.environ:
        return os.environ[env_var]
    else:
        raise Exception("No {} argument provided, can't connect".format(env_var))

cursor = None
cnx = None
def connect_to_db():
    #TODO Handle connexion error
    sql_params = {env_var: get_env(env_var) for env_var in
            ["MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST"]}
    global cnx
    cnx = mysql.connector.connect(user=sql_params["MYSQL_USER"],
                                  host=sql_params["MYSQL_HOST"],
                                  password=sql_params["MYSQL_PASSWORD"],
                                  database=sql_params["MYSQL_DATABASE"])

    global cursor
    cursor = cnx.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users("
            "user_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "user_name VARCHAR(255) NOT NULL UNIQUE,"
            "password BINARY(32) NOT NULL)"
        "DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin")

import pika
channel = None

def start_pika():
    if "RABBITMQ_HOST" in os.environ:
        host_dest = os.environ["RABBITMQ_HOST"]
    else:
        host_dest = "localhost"
    connection = pika.BlockingConnection(pika.ConnectionParameters(host_dest, heartbeat=0))
    global channel
    channel = connection.channel()
    channel.queue_declare(queue="web-queries")

connect_to_db()
start_pika()
