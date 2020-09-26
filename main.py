from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods = ['GET'])
def Home():
	return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
	fuel_type_d = 0
	if request.method == 'POST':
		year = int(request.form['Year'])
		curr_price = float(request.form['Present_Price'])
		km_driven = int(request.form['Kms_Driven'])
		km_driven = np.log(km_driven)
		owner = int(request.form['Owner'])
		fuel_type_p = request.form['Fuel_Type_Petrol']
		if (fuel_type_p == 'Petrol'):
			fuel_type_p = 1
			fuel_type_d = 0
		elif (fuel_type_p == 'Diesel'):
			fuel_type_p = 0
			fuel_type_d = 1
		else:
			fuel_type_p = 0
			fuel_type_d = 0
		year = 2020-year
		seller_type_individual = request.form['Seller_Type_Individual']
		if (seller_type_individual == 'Individual'):
			seller_type_individual = 1
		else:
			seller_type_individual = 0
		transmission_man = request.form['Transmission_Manual']
		if transmission_man == 'Manual':
			transmission_man = 1
		else:
			transmission_man = 0
		prediction = model.predict([[year,curr_price, km_driven, owner,
		fuel_type_d, fuel_type_p, seller_type_individual,
		transmission_man]])
		output = round(prediction[0], 2)
		print(output)
		if output < 0 :
			return render_template('index.html', prediction_text = "Sorry you cannot sell")
		else:
			return render_template('index.html', prediction_text = "You can sell the car at {}".format(output))
	else:
		return render_template('index.html')
if __name__ == "__main__":
	app.run(debug= True)
	   
		