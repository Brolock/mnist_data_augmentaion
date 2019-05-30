from flask import Flask
from flask import request

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
        userid = request.form['userid']
        number = request.form['number']
        return "You enter userid={} and number={}".format(userid, number)
