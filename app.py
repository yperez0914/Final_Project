from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
import pandas as pd 
import requests
import json
from config import lw_key
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta, datetime
from sklearn.svm import SVC 
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/forecast_db"
mongo = PyMongo(app)
url= "https://api.worldweatheronline.com/premium/v1/weather.ashx?"
past_url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx?"


# Route for home page
"""
Returns HTML with JS that takes in zipcode/dates
and feeds them to next route
"""
@app.route("/")
def home():
    return render_template("index.html")


# Route that intakes dates and zipcodes
"""
Historical weather and migraine history, combine
them into a df, store that df in mongo
"""
@app.route("/userdata/<dates>/<zipcode>")
def createUser(dates, zipcode):
    id = uuid.uuid4()
    zipcode = zipcode
    dates= dates
    dates=dates.split(",")
    dates= [i.strip() for i in dates]
    dates_df = pd.DataFrame(dates,columns=['Dates'])
    dates_df["Migraine"] = 1
    history_dict ={
    "Dates":[],
    "Cloudcover":[],
    "Humidity":[],
    "PrecipInch":[],
    "Pressure":[],
    "FeelsLike":[],
    "HeatIndex":[],
    "MaxTemp":[],
    "MinTemp":[],
    "SunHours":[],
    "UVIndex":[],
    }

    for i in range(6,0,-1):
        date= (datetime.today()-relativedelta(months=i)).strftime('%Y-%m-%d')
        enddate=(datetime.today()-relativedelta(months=i-1)).strftime('%Y-%m-%d')
        responses = requests.get(f"{past_url}key={lw_key}&q={zipcode}&date={date}&enddate={enddate}&tp=24&mca=no&aqi=yes&format=json").json()
        responses = responses['data']
        history_dict["Dates"].append([responses["weather"][i]["date"] for i in range(len(responses["weather"]))])
        history_dict["Cloudcover"].append([responses["weather"][i]["hourly"][0]["cloudcover"] for i in range(len(responses["weather"]))])
        history_dict["Humidity"].append([responses["weather"][i]["hourly"][0]["humidity"] for i in range(len(responses["weather"]))])
        history_dict["PrecipInch"].append([responses["weather"][i]["hourly"][0]["precipInches"] for i in range(len(responses["weather"]))])
        history_dict["Pressure"].append([responses["weather"][i]["hourly"][0]["pressure"] for i in range(len(responses["weather"]))])
        history_dict["FeelsLike"].append([responses["weather"][i]["hourly"][0]["FeelsLikeF"] for i in range(len(responses["weather"]))])
        history_dict["HeatIndex"].append([responses["weather"][i]["hourly"][0]["HeatIndexF"] for i in range(len(responses["weather"]))])
        history_dict["MaxTemp"].append([responses["weather"][i]["maxtempF"] for i in range(len(responses["weather"]))])
        history_dict["MinTemp"].append([responses["weather"][i]["mintempF"] for i in range(len(responses["weather"]))])
        history_dict["SunHours"].append([responses["weather"][i]["sunHour"] for i in range(len(responses["weather"]))])
        history_dict["UVIndex"].append([responses["weather"][i]["hourly"][0]["uvIndex"] for i in range(len(responses["weather"]))])

    history_df= pd.DataFrame.from_dict(history_dict,orient='index').transpose()
    history_df= history_df.apply(pd.to_numeric, errors= 'ignore')

    history_df= history_df.apply(pd.Series.explode).reset_index(drop=True)
    history_df= history_df.apply(pd.to_numeric, errors= 'ignore')
    history_df.reset_index(drop=True)
    history_df["TempDelta"]= history_df.MaxTemp - history_df.MinTemp
    history_df["BarChange"]= history_df["Pressure"].pct_change()
    history_df["HeatChange"]= history_df["HeatIndex"].pct_change()
    history_df["HumChange"]= history_df["Humidity"].pct_change()
    history_df= pd.merge(history_df,dates_df, on = 'Dates', how = 'left')
    history_df= history_df.fillna(0)
    history_df= history_df.iloc[1:]
    # history_data = json.loads(history_df.to_json(orient = "records"))
    collection = mongo.db.history
    history_df.reset_index(inplace=True)
    data_dict = history_df.to_dict("records")
    collection.insert_many(data_dict)
    print("Data inserted")
    return "Data inserted"
# Route to show second page (forecast)
"""
HTML and JS that loads data from the next route
"""
# Route to load data, perform ML, give predictions
"""
Import data from Mongo, perform ML, make predictions
return JSONIFIED data with weather, predictions, and anything else.
"""
@app.route("/predictions")
def forecast_call_ml():
    # url= "https://api.worldweatheronline.com/premium/v1/weather.ashx?"
    zipcode = input("Enter 5-digit Zipcode:")
    response = requests.get(f"{url}key={lw_key}&q={zipcode}&num_of_days=7&tp=24&mca=no&aqi=yes&format=json").json()
    response = response["data"]
    weather_dict ={
    "Dates":[],
    "Cloudcover":[],
    "Humidity":[],
    "PrecipInch":[],
    "Pressure":[],
    "FeelsLike":[],
    "HeatIndex":[],
    "MaxTemp":[],
    "MinTemp":[],
    "SunHours":[],
    "UVIndex":[],
    }

    weather_dict["Dates"]= ([response["weather"][i]["date"] for i in range(len(response["weather"]))])
    weather_dict["Cloudcover"]=([response["weather"][i]["hourly"][0]["cloudcover"] for i in range(len(response["weather"]))])
    weather_dict["Humidity"]= ([response["weather"][i]["hourly"][0]["humidity"] for i in range(len(response["weather"]))])
    weather_dict["PrecipInch"]= ([response["weather"][i]["hourly"][0]["precipInches"] for i in range(len(response["weather"]))])
    weather_dict["Pressure"]= ([response["weather"][i]["hourly"][0]["pressure"] for i in range(len(response["weather"]))])
    weather_dict["FeelsLike"]= ([response["weather"][i]["hourly"][0]["FeelsLikeF"] for i in range(len(response["weather"]))])
    weather_dict["HeatIndex"]= ([response["weather"][i]["hourly"][0]["HeatIndexF"] for i in range(len(response["weather"]))])
    weather_dict["MaxTemp"]= ([response["weather"][i]["maxtempF"] for i in range(len(response["weather"]))])
    weather_dict["MinTemp"]=([response["weather"][i]["mintempF"] for i in range(len(response["weather"]))])
    weather_dict["SunHours"]=([response["weather"][i]["sunHour"] for i in range(len(response["weather"]))])
    weather_dict["UVIndex"]= ([response["weather"][i]["hourly"][0]["uvIndex"] for i in range(len(response["weather"]))])
    weather_df= pd.DataFrame.from_dict(weather_dict,orient='index').transpose()
    weather_df= weather_df.apply(pd.to_numeric, errors= 'ignore')
    weather_df["TempDelta"] = weather_df.MaxTemp - weather_df.MinTemp
    weather_df["BarChange"] =weather_df["Pressure"].pct_change()
    weather_df["HeatChange"] =weather_df["HeatIndex"].pct_change()
    weather_df["HumChange"] =weather_df["Humidity"].pct_change()
    weather_df= weather_df.iloc[1:]
    new_migraine_df = weather_df.drop("Dates", axis =1)

    forecast_data = json.loads(weather_df.to_json(orient = "records"))
   
    #Pull data from MongoDB
    collection = mongo.db.history
    history_df = pd.DataFrame(list(collection.find()))
    #Pre-Processing of Data
    hist_ml_df= history_df.drop(columns =["Dates","_id","index"])
    # Assign X (data) and y (target)
    X = hist_ml_df.drop("Migraine", axis=1)
    y = hist_ml_df["Migraine"]
    print(X.shape, y.shape)
    #Split our data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    #Fit on the training data, use StandardScaler 
    X_scaler = StandardScaler().fit(X_train)
    X_scaler.get_params()
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    print(f"y_train value counts: {y_train.value_counts}")
    print(f"y_test value counts: {y_test.value_counts}")
    #Model creation
    model = SVC(kernel="linear")
    # Create the GridSearch estimator along with a parameter object containing the values to adjust
    param_grid = {'C': [1, 5, 10, 50],
                'gamma': [0.0001, 0.0005, 0.001, 0.005]}
    grid = GridSearchCV(model, param_grid, verbose=3)
    # Fit the model using the grid search estimator.This will take the SVC model and try each combination of parameters
    grid.fit(X_train_scaled, y_train)
    # List the best parameters for this dataset
    print(grid.best_params_)
    # List the best score
    print(grid.best_score_)
    # print(grid.score({X_test_scaled}, {y_test}))
    #Use model to make predictions with the hypertuned model
    predictions = grid.predict(X_test_scaled)
    # Run model on forecast data to formulate predictions
    X_new_scaled =X_scaler.transform(new_migraine_df)
    forecast_predictions = grid.predict(X_new_scaled)
    print(f"`forecast_predictions{forecast_predictions}")
    lists = forecast_predictions.tolist()
    json_str = json.dumps(lists)
    print("Predictions inserted")

    # render an index.html template and pass it the data you retrieved from the database
    return (f"We did it! Machine learning achieved! {forecast_data} {json_str}")
    # return render_template("results_index.html", forecast_predictions = forecast_predictions, forecast_data = forecast_data)

if __name__ == "__main__":
    app.run(debug=True)