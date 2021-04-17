from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
import pandas as pd 
import json
import uuid

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/forecast_db"
mongo = PyMongo(app)

@app.route("/userdata")
def createUser():
    id = uuid.uuid4()
    collection = mongo.db.user_data
    collection.insert_one(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)