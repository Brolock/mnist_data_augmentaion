from flask import Flask
from flask import request

import json
import os

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
        userid = request.form['user_id']
        number = request.form['number']
        channel.basic_publish(exchange='',
                              routing_key='web-queries',
                              body=json.dumps({"user_id": userid,"number": number}))
        return "You enter userid={} and number={}\n".format(userid, number)

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

start_pika()
