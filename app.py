from flask import Flask, render_template
from flask_jsonpify import jsonpify
import pymongo
import pandas as pd 
import requests
import json
from config import YP_API_KEY
from datetime import date, timedelta
# import geopy
import pgeocode
nomi = pgeocode.Nominatim('US')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
#create function for API call in route
@app.route("/")
def index():
    url= "https://api.openweathermap.org/data/2.5/onecall?"
    file = "mdzips.csv"
    df = pd.read_csv(file)
    md_zips = df['ZIPCODE1'].apply(nomi.query_postal_code)
    weather_dict ={
    "Zipcode": [],
    "Dates":[],
    "Pressure":[]
    }

    for i in range(len(md_zips.index)):
        response = requests.get(f"{url}lat={md_zips['latitude'][i]}&lon={md_zips['longitude'][i]}&exclude=current,minutely,hourly,alerts&appid={YP_API_KEY}").json()
        weather_dict["Zipcode"].append(md_zips["postal_code"][i])
        weather_dict["Dates"].append([response["daily"][i]["dt"] for i in range(len(response["daily"]))])
        weather_dict["Pressure"].append([response["daily"][i]["pressure"] for i in range(len(response["daily"]))])
        
    weather_df =pd.DataFrame.from_dict(weather_dict, orient = 'index')
    weather_df = weather_df.transpose()
    weather_df[[f"{date.today()}", f"{date.today()+timedelta(1)}", f"{date.today()+timedelta(2)}", f"{date.today()+timedelta(3)}", f"{date.today()+timedelta(4)}", f"{date.today()+timedelta(5)}", f"{date.today()+timedelta(6)}", f"{date.today()+timedelta(7)}"]]= pd.DataFrame(weather_df.Pressure.to_list(), index = weather_df.index)
    forecast = weather_df.drop(columns= ["Dates","Pressure"])
    result = json.loads(forecast.to_json(orient = 'records'))
    weather_api = json.dumps(result, indent =200)
    return (weather_api)
    # return render_template('index.html', weather_api=weather_api)
    
    # result = forecast.values.tolist()
    # JSONP_data= jsonpify(result)
    # return(JSONP_data) 
    # return jsonify()
# setup mongo connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

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