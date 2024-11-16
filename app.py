import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

app = Flask("Heart_Disease_Prediction")

# Loading the model
model_file = 'best_model.pkl'
with open(model_file, 'rb') as file_out:
    model = pickle.load(file_out)

columns = [
    "male", "age", "education", "currentsmoker", "cigsperday", "bpmeds", "prevalentstroke", 
    "prevalenthyp", "diabetes", "totchol", "bmi", "heartrate", "glucose"
]

@app.route('/', methods=['GET'])
def home_page():
    return "Welcome to Heart Disease Prediction!"

@app.route('/predict', methods=['POST'])
def predict():
    
    patient = request.get_json()

    patient_values = list(patient.values())
    patient_df = pd.DataFrame([patient_values], columns=columns)

    # Make the prediction
    prediction = model.predict(patient_df)[0]  # Get the prediction (0 or 1)

    # Heart disease risk classification logic
    if prediction == 0:
        risk_classification = "Low Risk"  # Low risk of heart disease
    else:
        risk_classification = "High Risk"  # High risk of heart disease

    # Result dictionary
    result = {
        "DiagnosisValue": int(prediction),
        "RiskClassification": risk_classification
    }

    # Return the result as JSON
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
