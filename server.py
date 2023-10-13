from flask import Flask, request,jsonify
#import util
app=Flask(__name__)



@app.route('/get_location_names' ,methods=['GET','POST'])

def get_location_names():
        response=jsonify({
            'locations':get_location_names()
        })
        print(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
   
    
    
    
    
@app.route('/predict_home_price', methods=['GET','POST'])
def predict_home_price():
    total_sqft=float(request.form['total_sqft'])
    location=request.form['location']
    bhk=int(request.form['bhk'])
    bath=int(request.form['bath'])
    
    
    response=jsonify({
            'estimated_price':get_estimated_price(location, total_sqft, bhk, bath)
            })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

import json
import pickle
import numpy as np


__locations=None
__data_columns=None
__model=None

def get_estimated_price(location,sqft,bhk,bath):
    
    try:
        
       loc_index = __data_columns.index(location.lower())
    except:
        loc_index=-1
    
    
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    
    return round( __model.predict([x])[0],2)
    




def load_saved_artifacts():
    print("loading saved artifacts")
    global __data_columns
    global __locations
    
    with open("./artifacts/columns.json",'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
        
    global __model    
    with open("./artifacts/banglore_home_prices_model.pickle",'rb') as f:
        __model = pickle.load(f)
    print("loading saved artifacts....")
    
    
def get_location_names():
    load_saved_artifacts()
    return __locations
    









  

if __name__=="__main__":
    print("Starting python Flask server for home price prediction..")
    app.run(debug=True)