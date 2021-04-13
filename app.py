from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
import pandas as pd 
import requests
import json
from config import YP_API_KEY, lw_key
from datetime import date, timedelta
# import geopy
import pgeocode
nomi = pgeocode.Nominatim('US')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/forecast_db"
mongo = PyMongo(app)
#create function for API call in route
@app.route("/forecast_data")
def forecast_load():
    url= "https://api.worldweatheronline.com/premium/v1/weather.ashx?"
    zipcode = input("Enter 5-digit Zipcode:")
    response = requests.get(f"{url}key={lw_key}&q={zipcode}&num_of_days=7&tp=24&mca=no&aqi=yes&format=json").json()
    # result = json.loads(forecast.to_json(orient = 'records'))
    # forecast_api = json.dumps(response, indent =200)
    #    return (forecast_api)
    # return render_template('index.html', weather_api=weather_api)

    # Use flask_pymongo to set up mongo connection
    collection = mongo.db.final
    collection.insert_one(response)
    print("Data inserted")
    return "Try it" # jsonify(response)

@app.route("/history")
def history():
    past_url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx?"
    zipcode = input("Enter 5-digit Zipcode:")
    dates= input("Dates you had a migraine (YYYY-MM-DD):")
    dates_split = dates.split(",")
    for date in dates_split:
        responses = requests.get(f"{past_url}key={lw_key}&q={zipcode}&date={date}&tp=24&mca=no&aqi=yes&format=json").json()
    collection = mongo.db.history
    collection.insert_one(responses)
    print("Data inserted")
    return "History"
# # connect to mongo db and collection
# db = client.store_inventory
# produce = db.produce
# @app.route("/predictions")
# def mlearn():
    
#     # write a statement that finds all the items in the db and sets it to a variable
#     inventory = list(produce.find())
#     print(inventory)

#     # render an index.html template and pass it the data you retrieved from the database
#     return render_template("index.html", inventory=inventory)


if __name__ == "__main__":
    app.run(debug=True)