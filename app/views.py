from app import app, collection
from flask import render_template, redirect, url_for

@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    data = []
    for i in collection.find():
        data.append(i)
    return render_template("index.html", data=data)




